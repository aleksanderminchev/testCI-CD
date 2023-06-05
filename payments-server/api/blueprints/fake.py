from re import S
import click
import csv
import datetime
from dateutil.relativedelta import relativedelta
from flask import Blueprint
from faker import Faker
from api.app import db
from models.user import User
from models.admin import Admin
from models.teacher import Teacher
from models.student import Student
from models.lesson import Lesson
from models.customer import Customer
from models.balance import Balance
from models.interest import Interest
from models.subjects import Subjects
from models.language import Language
from models.qualification import Qualification
from models.higher_education_institution import HigherEducationInstitution
from models.high_school import HighSchool
from models.program import Program
from models.higher_education_programme import HigherEducationProgramme
from models.wagepayment import WagePayment
from models.referral import Referral
from models.order import Order
from models.transaction import Transaction
from api.utils.lessonspace import create_lesson_space
fake = Blueprint('fake', __name__)
faker = Faker()


@fake.cli.command()
@click.argument('num', type=int)
def users(num):  # pragma: no cover
    """Create the given number of fake customers with attached students.
    E.g. flask fake customers_teachers_students 10. Will create 5 independent and 5 family customers."""

    # Creating fake families with an attached student
    for i in range(num):
        email = faker.email()
        password = faker.password()

        student_data = {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            'gender': "male",
            'student_type': 'child',
        }

        Customer.add_customer_user(
            email=email,
            password=password,
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            phone=faker.phone_number(),
            customer_type='family'
        )

        Customer.add_student_to_family(email=email, student_data=student_data)

    for i in range(num):
        customer = Customer.add_independent_customer_with_student(
            email=faker.email(),
            password=faker.password(),
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            phone=faker.phone_number(),
            customer_type='independent'
        )

        # tutor_mail = faker.email()
        # Teacher.add_new_teacher(data={
        #     "email": tutor_mail,
        #     "password": faker.password(),
        #     "first_name": faker.first_name(),
        #     "last_name": faker.last_name(),
        #     "phone": faker.phone_number()}
        # )
        # Teacher.add_student_to_teacher(customer["student"].id, tutor_mail)

    db.session.commit()


@fake.cli.command()
@click.argument('filename', type=str)
def tutors(filename):  # pragma: no cover
    """Upload teachers from a CSV file.
    Run this in CLI: flask fake tutors FILENAME.csv"""

    # Reading the CSV file
    with open(filename, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file, delimiter=";")
        # Iterate through each row in the CSV file
        for row in csv_reader:
            from pprint import pprint
            pprint(row)
            # Perform validations and transformations
            first_name = row["First Name"]
            last_name = row["Last Name"]
            email = row["Email"].lower()

            # Remove spaces in phone number
            phone = row["Mobile Phone"].replace(
                " ", "").replace("(", "").replace(")", "")

            if not phone.startswith("+"):
                phone = "+45" + phone
            if len(phone) != 11:
                print("ERROR: PHONE NOT 11 CHARS.", phone)
                print("Tutor:", first_name, last_name)

            open_for_new_students = True
            if row["Vil du have flere forløb?"] == "Jeg vil ikke have flere forløb i øjeblikket":
                open_for_new_students = False

            payroll_id = row["CPR-nr (DDMMÅÅ-XXXX)"].replace("-", "")

            # Only get the digits
            reg_and_bank_digits = ''.join(
                char for char in row["Reg nr. og konto nr. (f.eks. XXXX-XXXXXXXXXX)"] if char.isdigit())

            # the first 4 digits is the reg number and the rest is bank number
            reg_number = reg_and_bank_digits[:4]

            # The rest after the reg number
            bank_number = reg_and_bank_digits[4:]

            finished_highschool = False
            if row["Går du stadig på gymnasiet eller ej? "] == "Jeg er færdig med gymnasiet":
                finished_highschool = True

            string_to_value_mapping = {
                "7 til 8": 7,
                "8 til 9": 8,
                "9 til 10": 9,
                "10 til 11": 10,
                "11 til 12": 11,
                "Over 12": 12,
            }

            grade_average = string_to_value_mapping.get(
                row["Karaktergennemsnit"], 0)

            genders = {
                "Mand": "male",
                "Kvinde": "female"
            }
            gender = genders.get(row["Køn"])

            # If empty string then make it Null
            birthday = row["Birth Date"]
            if birthday == "":
                birthday = None

            user = User(
                email=email,
                password="",
                first_name=first_name,
                last_name=last_name,
                phone=phone
            )

            db.session.add(user)
            db.session.commit()

            teacher = Teacher(
                user_id=user.uid,
                wage_per_hour=150,
                bio=row["Bio"],
                status=row["Status"].lower(),
                country=row["Country"] or "Denmark",
                address=row["Address"],
                city=row["City"],
                zip_code=row["Zip"],
                gender=gender,
                created_on_tw_at=row["Created at"],
                updated_on_tw_at=row["Updated at"],
                open_for_new_students=open_for_new_students,
                birthday=birthday,
                bank_number=bank_number,
                reg_number=reg_number,
                teachworks=row["Profile ID"],
                payroll_id=payroll_id,
                grade_average=grade_average,
                internal_note=row["Intern note"],
                how_they_found=row["Hvor har du hørt om os? "],
                finished_highschool=finished_highschool,
                inactive_reason=row["Grund til tutor stopper "],
                application_reason=row["Hvorfor valgte du at ansøge hos TopTutors?"],
            )

            # Get the string of comma seperated subjects
            subjects = row["Subjects"]
            # Split the comma-separated string into a list of subject names
            subject_names = list(set([name.strip()
                                      for name in subjects.split(',') if name.strip()]))

            subjects = []
            for name in subject_names:
                subject = db.session.query(
                    Subjects).filter_by(name=name).first()
                if not subject:
                    raise NameError("SUBJECT NAME DOES NOT EXIST ", name)

                subjects.append(subject)

            # Assign the Subject instances to the Teacher instance
            teacher.subjects = subjects

            # Get the string of comma seperated programs
            programs = row["Programmer du kan anvende"]
            # Split the comma-separated string into a list of program names
            names = [name.strip()
                     for name in programs.split(',') if name.strip()]

            programs = []
            for name in names:
                program = db.session.query(
                    Program).filter_by(name=name).first()
                if not program:
                    raise NameError("PROGRAM NAME DOES NOT EXIST ", name)

                programs.append(program)

            # Assign the Program instances to the Teacher instance
            teacher.programs = programs

            # Get the string of comma seperated languages
            langs = row["Vælg de sprog du er helt flydende i"]
            # Split the comma-separated string into a list of language names
            names = [name.strip()
                     for name in langs.split(',') if name.strip()]

            langs = []
            for name in names:
                if name == "Persisk":
                    name = "Farsi"
                lang = db.session.query(
                    Language).filter_by(name=name).first()
                if not lang:
                    raise NameError("LANGUAGE NAME DOES NOT EXIST ", name)

                langs.append(lang)

            # Assign the Program instances to the Teacher instance
            teacher.languages = langs

            # Get the string of comma seperated interests
            interests = row["Hvad er dine interesser?"]
            # Split the comma-separated string into a list of interests names
            names = [name.strip()
                     for name in interests.split(',') if name.strip()]

            interests = []
            for name in names:
                interest = db.session.query(
                    Interest).filter_by(name=name).first()
                if not interest:
                    raise NameError("INTEREST NAME DOES NOT EXIST ", name)

                interests.append(interest)

            # Assign the Program instances to the Teacher instance
            teacher.interests = interests

            # Get the string of comma seperated interests
            qualifications = row["Kendetegn / Kvalifikationer "]
            # Split the comma-separated string into a list of qualifications names
            names = [name.strip()
                     for name in qualifications.split(',') if name.strip()]

            qualifications = []
            for name in names:
                if name in ["Engelsk korrektur/grammatik", "God til sprogundervisning", "Dansk korrektur/grammatik", "Ikke særlig pædagogisk"]:
                    continue
                qualification = db.session.query(
                    Qualification).filter_by(name=name).first()
                if not qualification:
                    raise NameError("qualification NAME DOES NOT EXIST ", name)

                qualifications.append(qualification)

            # Assign the Program instances to the Teacher instance
            teacher.qualifications = qualifications

            # Add higher education programme
            name = row["Hvis du går på en videregående uddannelse. Hvilken uddannelse læser du så på?"]
            higher_education = db.session.query(
                HigherEducationProgramme).filter_by(name=name).first()
            if higher_education is not None:
                teacher.higher_education_programmes = [higher_education]

            # Add higher education institution
            name = row["Videregående uddannelsesinstitution"]
            higher_education = db.session.query(
                HigherEducationInstitution).filter_by(name=name).first()
            if higher_education is not None:
                teacher.higher_education_institutions = [higher_education]

            db.session.add(teacher)
            db.session.commit()
            print(first_name, " ", last_name, " successfully added")

            # Add high school
            name = row["Gymnasietype "]
            high_school = db.session.query(
                HighSchool).filter_by(name=name).first()
            if high_school is not None:
                teacher.high_school = [high_school]

            db.session.add(teacher)
            db.session.commit()
            print(first_name, " ", last_name, " successfully added")

    print("All tutors have been added")


@fake.cli.command()
@click.argument('email', type=str)
def admin(email):  # pragma: no cover
    """Create an admin user with given email.
    Run this in CLI with flask fake admin yourmail@domain.com"""
    admin = Admin.add_new_admin(email=email, password="admin")
    print(admin)
    print(email, ' admin added.')


@fake.cli.command()
def independent():  # pragma: no cover
    email = faker.email()
    password = faker.password()

    customer = Customer.add_independent_customer_with_student(
        email=email, password=password, customer_type="independent")
    print(customer)


@fake.cli.command()
def family():  # pragma: no cover
    email = faker.email()
    password = faker.password()

    user = User(email=email, password=password)
    db.session.add(user)
    db.session.commit()

    customer = Customer(user_id=user.uid, customer_type="independent")
    db.session.add(customer)
    db.session.commit()

    student = Student(customer_id=customer.id)
    db.session.add(student)
    db.session.commit()
    print(email, ' user added.')


@fake.cli.command()
@click.argument("email", type=str)
def get(email):
    tutor = Tutor.get_from_kwarg(db.session, email=email)


@fake.cli.command()
def test():  # pragma: no cover
    pass


@fake.cli.command()
def customer():  # pragma: no cover
    email = faker.email()
    password = "admin"

    user = User(email=email, password=password)
    db.session.add(user)
    db.session.commit()

    customer = Customer(user_id=user.uid, customer_type="family")
    db.session.add(customer)
    db.session.commit()

    print(user.customer)
    print(user.customer.to_dict())

    print(email, ' user added.')


@fake.cli.command()
def teacher():  # pragma: no cover
    email = "teacher@toptutors.dk"
    password = "admin"

    user = User(email=email, password=password)
    db.session.add(user)
    db.session.commit()

    teacher = Teacher(user_id=user.uid)
    db.session.add(teacher)
    db.session.commit()

    print(email, ' teacher added.')


@fake.cli.command()
def interests():  # pragma: no cover
    interests = [
        Interest(name="Fodbold"),
        Interest(name="Computerspil"),
        Interest(name="Musik"),
        Interest(name="Programmering"),
        Interest(name="Ridning"),
        Interest(name="Håndbold"),
        Interest(name="Teater"),
        Interest(name="Kunst"),
        Interest(name="Politik"),
        Interest(name="Svømning"),
        Interest(name="Læsning"),
        Interest(name="Gymnastik"),
        Interest(name="Badminton"),
        Interest(name="Tegne"),
        Interest(name="Male"),
        Interest(name="Elsker dyr"),
        Interest(name="Ballet"),
        Interest(name="Yoga"),
        Interest(name="Billedkunst"),
        Interest(name="Klaver"),
        Interest(name="Boksning"),
        Interest(name="Ishockey"),
        Interest(name="Basketball"),
    ]

    db.session.bulk_save_objects(interests)
    db.session.commit()

    print("Added interests")


@fake.cli.command()
def subjects():  # pragma: no cover
    subjects = ["Afsætning A", "Afsætning B", "Afsætning C", "Almen sprogforståelse", "Antropologi", "Arabisk A", "Arabisk B", "Arabisk C", "Astronomi C", "Billedkunst B", "Billedkunst C", "Biologi A", "Biologi B", "Biologi C", "Biologi Folkeskole", "Bioteknologi A", "Bioteknologi B", "Bioteknologi C", "Byggeri og Energi (Byg A)", "Dans C", "Dansk A", "Dansk B", "Dansk C", "Dansk Folkeskole", "Datalogi C", "Design B", "Design C", "Design og arkitektur B", "Design og arkitektur C", "Design og Produktion", "DHO", "Digitalt design og udvikling A", "Dramatik B", "Dramatik C", "Engelsk A", "Engelsk B", "Engelsk C", "Engelsk Folkeskole", "Environmental Systems", "Erhvervscase", "Erhvervsret C", "Erhvervsøkonomi C", "Filosofi B", "Filosofi C", "Finansiering B", "Finansiering C", "Forsikring og Jura", "Fransk A", "Fransk B", "Fransk C", "Fransk Folkeskole", "Fysik A", "Fysik B", "Fysik C", "Fysik/kemi Folkeskole", "Geografi C", "Geografi Folkeskole", "Geovidenskab A", "Global Politics", "Græsk A", "Græsk C", "Historie A", "Historie B", "Historie C", "Historie Folkeskole", "IB English", "IB Spanish", "Idehistorie B", "Idehistorie C", "Idræt B", "Idræt C", "Informatik B", "Informatik C", "Informationsteknologi B", "Informationsteknologi C", "Innovation B", "Innovation C", "International teknologi og kultur C", "International økonomi A",
                "International økonomi B", "International økonomi C", "It A", "It B", "Italiensk A", "Italiensk B", "Italiensk C", "Japansk A", "Japansk B", "Kemi A", "Kemi B", "Kemi C", "Kinesisk A", "Kinesisk B", "Kinesisk C", "Kommunikation/it A", "Kommunikation/it B", "Kommunikation/it C", "Kristendom Folkeskole", "Kulturforståelse B", "Kulturforståelse C", "Latin A", "Latin B", "Latin C", "Markedskommunikation C", "Matematik A", "Matematik B", "Matematik C", "Matematik Folkeskole", "Materialeteknologi C", "Mediefag B", "Mediefag C", "Multimedier C", "Musik A", "Musik B", "Musik C", "Musik og lydproduktion C", "Natur/teknik Folkeskole", "Naturgeografi B", "Naturgeografi C", "Naturvidenskabelig faggruppe", "Naturvidenskabelige grundforløb (NV)", "Oldtidskundskab C", "Organisation C", "Bioteknologi og mikrobiologi A", "Fødevarer A", "Miljøteknik A", "Procesteknologi og kemisk industri A", "Sundhed & Træning A", "Proces levnedsmiddel og sundhed A", "Produktudvikling C", "Programmering B", "Programmering C", "Psykologi B", "Psykologi C", "Religion B", "Religion C", "Retorik C", "Russisk A", "Samfundsfag A", "Samfundsfag B", "Samfundsfag C", "Samfundsfag Folkeskole", "Samtidshistorie B", "SOP", "Spansk A", "Spansk B", "Spansk C", "Spansk Folkeskole", "SRP", "Statistik C", "Teknologi A", "Teknologi B", "Teknologihistorie C", "Tyrkisk A", "Tyrkisk B", "Tysk A", "Tysk B", "Tysk C", "Tysk Folkeskole", "Virksomhedsøkonomi A", "Virksomhedsøkonomi B", "Virksomhedsøkonomi C"]

    subjects_objects = [Subjects(name=name) for name in subjects]

    db.session.bulk_save_objects(subjects_objects)
    db.session.commit()

    print("Added all subjects")


@fake.cli.command()
def languages():  # pragma: no cover
    languages = ["Engelsk",
                 "Tysk",
                 "Fransk",
                 "Spansk",
                 "Arabisk",
                 "Portugisisk",
                 "Russisk",
                 "Japansk",
                 "Kinesisk",
                 "Italiensk",
                 "Tyrkisk",
                 "Ukrainsk",
                 "Islandsk",
                 "Norsk",
                 "Svensk",
                 "Hindi",
                 "Farsi",
                 "Græsk",
                 "Hollandsk",
                 "Polsk"]

    objects = [Language(name=name) for name in languages]

    db.session.bulk_save_objects(objects)
    db.session.commit()

    print("Added all languages")


@fake.cli.command()
def qualifications():  # pragma: no cover
    qualifications = ["Erfaring med ordblindhed", "Erfaring med ADHD", "Erfaring med talblindhed", "Erfaring med autisme",
                      "Erfaring med angst", "Erfaring med depression", "God med de yngste børn i indskoling", "God til gymnasieforløb", "Super pædagogisk"]

    objects = [Qualification(name=name) for name in qualifications]

    db.session.bulk_save_objects(objects)
    db.session.commit()

    print("Added all qualifications")


@fake.cli.command()
def institutions():  # pragma: no cover
    institutions = ["Københavns Universitet",
                    "Aarhus Universitet",
                    "Syddansk Universitet",
                    "Roskilde Universitet",
                    "Aalborg Universitet",
                    "Danmarks Tekniske Universitet",
                    "Copenhagen Business School",
                    "IT-Universitetet",
                    "Professionshøjskolen UCN",
                    "Via University College",
                    "UC Syd",
                    "Danmarks Medie- og Jornalisthøjskole",
                    "Københavns Professionshøjskole",
                    "Absalon Professionshøjskole",
                    "UCL Erhvervsakademi og Professionshøjskole",
                    "Copenhagen Business Academy",
                    "Erhvervsakademi Kolding",
                    "Erhvervsakademi Dania",
                    "Københavns Erhvervskademi",
                    "Zealand",
                    "Erhvervsakademi Midtvest",
                    "Erhvervsakademi Sydvest",
                    "Erhvervsakademi Aarhus",
                    "SmartLearning"]

    objects = [HigherEducationInstitution(name=name) for name in institutions]

    db.session.bulk_save_objects(objects)
    db.session.commit()

    print("Added all qualifications")


@fake.cli.command()
def highschool():  # pragma: no cover
    gym = ["STX", "HHX", "HTX", "HF", "IB", "IBB",
           "EUX", "EUD", "Udenlandsk gymnasium", "Andet"]

    objects = [HighSchool(name=name) for name in gym]

    db.session.bulk_save_objects(objects)
    db.session.commit()

    print("Added all high school types")


@fake.cli.command()
def programs():  # pragma: no cover
    programs = ["Maple",
                "TI-Nspire",
                "Geogebra",
                "Wordmat",
                "Excel",
                "Matlab",
                "STATA",
                "JMP",
                "R",
                "Python",]

    objects = [Program(name=name) for name in programs]

    db.session.bulk_save_objects(objects)
    db.session.commit()

    print("Added all math programs")


@fake.cli.command()
def educations():  # pragma: no cover
    educations = ["Går ikke på en videregående uddannelse",
                  "AP Graduate in Automation Engineering",
                  "AP Graduate in Automotive Technology",
                  "AP Graduate in Chemical and Biotechnical Science",
                  "AP Graduate in Commerce Management",
                  "AP Graduate in Computer Science",
                  "AP Graduate in Design Technology and Business",
                  "AP Graduate in IT Technology",
                  "AP Graduate in Logistic Management",
                  "AP Graduate in Marketing Management",
                  "AP Graduate in Multimedia Design",
                  "AP Graduate in Production Technology",
                  "AP Graduate in Service Hospitality and Tourism Management",
                  "Administrationsøkonom",
                  "Agrobiologi",
                  "Amerikanske Studier",
                  "Antropologi",
                  "Anvendt filosofi",
                  "Arabisk- og islamstudier",
                  "Arkitekt",
                  "Arkæologi",
                  "Asienstudier (japanstudier)",
                  "Asienstudier (kinastudier)",
                  "Asienstudier (koreastudier)",
                  "Audiologi",
                  "Audiologopædi",
                  "Automationsteknolog",
                  "Autoteknolog",
                  "Bachelor in Graphic Storytelling",
                  "Bachelor of Animation",
                  "Bachelor of Architectural Technology and Construction Management",
                  "Bachelor of Crafts in Glass and Ceramics",
                  "Bachelor of Economics and Information Technology",
                  "Bachelor of Engineering in Biotechnology",
                  "Bachelor of Engineering in Civil Engineering",
                  "Bachelor of Engineering in Climate and Supply Engineering",
                  "Bachelor of Engineering in Electronics",
                  "Bachelor of Engineering in Global Business Engineering",
                  "Bachelor of Engineering in Global Management and Manufacturing",
                  "Bachelor of Engineering in Mechanical Engineering",
                  "Bachelor of Engineering in Mechatronics",
                  "Bachelor of Export and Technology Management",
                  "Bachelor of Science (BSc) in Engineering (Applied Industrial Electronics)",
                  "Bachelor of Science (BSc) in Engineering (Chemical Engineering and Biotechnology)",
                  "Bachelor of Science (BSc) in Engineering (Electronics)",
                  "Bachelor of Science (BSc) in Engineering (Engineering Innovation and Business)",
                  "Bachelor of Science (BSc) in Engineering (General Engineering)",
                  "Bachelor of Science (BSc) in Engineering (Mechanical Engineering)",
                  "Bachelor of Science (BSc) in Engineering (Mechatronics)",
                  "Bachelor of Science (BSc) in Engineering (Product Development and Innovation)",
                  "Bachelor of Value Chain Management",
                  "Bachelor of financial management and services",
                  "Bibliotekskundskab og videnskommunikation",
                  "Biokemi",
                  "Biokemi og molekylær biologi",
                  "Biologi",
                  "Biomedicin",
                  "Bioteknologi",
                  "Brasilianske studier",
                  "Business Administration and Digital Management",
                  "Business Administration and Service Management",
                  "Business Administration and Sociology",
                  "Business Asian Language and Culture - International Business in Asia Chinese/English",
                  "Business Asian Language and Culture - International Business in Asia Japanese/English",
                  "Business Language and Culture",
                  "Byggekoordinator",
                  "Bygningskonstruktør professionsbachelor i bygningskonstruktion",
                  "Cognitive Science",
                  "Dansk",
                  "Data Science",
                  "Datalogi",
                  "Datalogi-økonomi",
                  "Datamatiker",
                  "Datavidenskab",
                  "Designer",
                  "Designkultur",
                  "Designkultur og økonomi",
                  "Designteknolog",
                  "Digital design - it æstetik og interaktion",
                  "Digital design og interaktive teknologier",
                  "Diplomingeniør Klima og forsyningsteknik",
                  "Diplomingeniør arktisk byggeri og infrastruktur",
                  "Diplomingeniør bioteknologi",
                  "Diplomingeniør byggeri og anlæg",
                  "Diplomingeniør byggeri og infrastruktur",
                  "Diplomingeniør bygning",
                  "Diplomingeniør bygningsdesign",
                  "Diplomingeniør bygningsteknik",
                  "Diplomingeniør bæredygtig energiteknik",
                  "Diplomingeniør eksport og teknologi",
                  "Diplomingeniør elektrisk energiteknologi",
                  "Diplomingeniør elektronik",
                  "Diplomingeniør elektroteknologi",
                  "Diplomingeniør fiskeriteknologi",
                  "Diplomingeniør forretningsudvikling (Business Development) BDE",
                  "Diplomingeniør fødevaresikkerhed og -kvalitet",
                  "Diplomingeniør globale forretningssystemer",
                  "Diplomingeniør integreret design",
                  "Diplomingeniør it og økonomi",
                  "Diplomingeniør it-elektronik",
                  "Diplomingeniør kemi (kemiteknik)",
                  "Diplomingeniør kemi og fødevareteknologi",
                  "Diplomingeniør kemi- og bioteknik",
                  "Diplomingeniør kemi- og bioteknologi",
                  "Diplomingeniør kemiteknik og International Business",
                  "Diplomingeniør maskinteknik",
                  "Diplomingeniør maskinteknologi",
                  "Diplomingeniør mobilitet transport og logistik",
                  "Diplomingeniør proces og innovation",
                  "Diplomingeniør produktion (produktionsteknik)",
                  "Diplomingeniør robotteknologi",
                  "Diplomingeniør softwareteknologi",
                  "Diplomingeniør sundhedsteknologi",
                  "Dramaturgi",
                  "Driftsteknolog - Offshore",
                  "Economics and Business Administration",
                  "Energiteknolog",
                  "Engelsk",
                  "Entreprenørskab og design",
                  "Erhvervsøkonomi med tilvalg",
                  "Erhvervsøkonomi og markeds- og kulturanalyse HA i markeds- og kulturanalyse",
                  "Erhvervsøkonomi HA",
                  "Erhvervsøkonomi HA (Projektledelse)",
                  "Erhvervsøkonomi-erhvervsret HA (jur.)",
                  "Erhvervsøkonomi-erhvervssprog (negot) (SDU - Odense)",
                  "Erhvervsøkonomi-filosofi HA (fil.)",
                  "Erhvervsøkonomi-informationsteknologi HA (it.)",
                  "Erhvervsøkonomi-jura HA (jur.)",
                  "Erhvervsøkonomi-matematik HA (mat.)",
                  "Erhvervsøkonomi-psykologi HA (psyk.)",
                  "Erhvervsøkonomi-virksomhedskommunikation HA (kom.)",
                  "European Studies",
                  "Europæisk business HA i europæisk business",
                  "Europæisk etnologi",
                  "Farmaci",
                  "Film- og medievidenskab",
                  "Filosofi",
                  "Financial controller",
                  "Finansøkonom",
                  "Folkesundhedsvidenskab",
                  "Forhistorisk arkæologi",
                  "Forsikringsmatematik",
                  "Fransk sprog og kultur",
                  "Fransk sprog litteratur og kultur",
                  "Fysik",
                  "Fødevarer og ernæring",
                  "Geografi",
                  "Geografi og geoinformatik",
                  "Geologi-geoscience",
                  "Geoscience",
                  "Global Business Informatics",
                  "Græsk klassisk",
                  "Grønlandske og arktiske studier",
                  "Handelsøkonom",
                  "Historie",
                  "Humanistisk bacheloruddannelse",
                  "Humanistisk bacheloruddannelse + journalistik + andet fag",
                  "Humanistisk international bacheloruddannelse",
                  "Humanistisk-teknologisk bacheloruddannelse",
                  "Humanistisk-teknologisk bacheloruddannelse + journalistik + andet fag",
                  "Husdyrvidenskab",
                  "Idræt",
                  "Idræt og fysisk aktivitet",
                  "Idræt og sundhed",
                  "Idrætsvidenskab",
                  "Idéhistorie",
                  "Indianske sprog og kulturer",
                  "Indien- og sydasienstudier",
                  "Informationsstudier",
                  "Informationsteknologi",
                  "Informationsvidenskab",
                  "Informationsvidenskab it og interaktionsdesign",
                  "Innovation og digitalisering",
                  "Installatør VVS",
                  "Installatør stærkstrøm",
                  "Interaktionsdesign",
                  "Interkulturel pædagogik og dansk som andetsprog",
                  "International Business",
                  "International Business and Politics",
                  "International Shipping and Trade",
                  "International erhvervsøkonomi med fremmedsprog",
                  "International virksomhedskommunikation i 2 fremmedsprog",
                  "International virksomhedskommunikation i engelsk",
                  "International virksomhedskommunikation i fransk",
                  "International virksomhedskommunikation i spansk",
                  "International virksomhedskommunikation i tysk",
                  "It-produktudvikling",
                  "It-teknolog",
                  "Japanstudier",
                  "Jordbrugsteknolog",
                  "Journalistik",
                  "Jura",
                  "Kemi",
                  "Kinastudier",
                  "Klassisk arkæologi",
                  "Klassisk filologi",
                  "Klinisk tandtekniker",
                  "Kommunikation og digitale medier",
                  "Kommunikation og it",
                  "Konservator",
                  "Kort- og landmålingstekniker",
                  "Kunst og teknologi",
                  "Kunsthistorie",
                  "Laborant",
                  "Landinspektørvidenskab",
                  "Landskabsarkitektur",
                  "Latin",
                  "Lingvistik",
                  "Litteraturhistorie",
                  "Litteraturvidenskab",
                  "Logistikøkonom",
                  "Machine learning og datavidenskab",
                  "Markedsføringsøkonom",
                  "Market and Management Anthropology",
                  "Matematik",
                  "Matematik og anvendt matematik",
                  "Matematik-økonomi",
                  "Medialogi",
                  "Medicin",
                  "Medicin med industriel specialisering",
                  "Medicinalkemi",
                  "Medievidenskab",
                  "Mellemøstens sprog og samfund (arabisk hebraisk persisk tyrkisk)",
                  "Mellemøstens sprog og samfund (assyriologi nærorientalsk arkæologi ægyptologi)",
                  "Miljø- og fødevareøkonomi",
                  "Miljøteknolog",
                  "Moderne Indien og Sydasienstudier",
                  "Molekylær biomedicin",
                  "Molekylær medicin",
                  "Molekylærbiologi",
                  "Multimediedesigner",
                  "Musik",
                  "Musikterapi",
                  "Musikvidenskab",
                  "Nanoscience",
                  "Naturressourcer",
                  "Naturvidenskabelig bacheloruddannelse",
                  "Naturvidenskabelig international bacheloruddannelse",
                  "Nordisk sprog og litteratur (dansk)",
                  "Odontologi",
                  "Oldtidskundskab",
                  "Organisatorisk læring",
                  "P Graduate in Computer Science",
                  "Politik og Administration",
                  "Politik og økonomi",
                  "Procesteknolog (ernærings- fødevare- mejeri- og procesteknologi)",
                  "Produktionsteknolog",
                  "Professionsbachelor Leisure Management",
                  "Professionsbachelor Multiplatform Storytelling and Production",
                  "Professionsbachelor beredskab katastrofe- og risikomanagement",
                  "Professionsbachelor bioanalytiker",
                  "Professionsbachelor dansk tegnsprog og tolkning",
                  "Professionsbachelor eksport og teknologi",
                  "Professionsbachelor ergoterapeut",
                  "Professionsbachelor ernæring og sundhed",
                  "Professionsbachelor finans",
                  "Professionsbachelor folkeskolelærer",
                  "Professionsbachelor fotojournalist",
                  "Professionsbachelor fremmedsprog og digital markedskommunikation",
                  "Professionsbachelor fysioterapeut",
                  "Professionsbachelor fødevareteknologi og applikation",
                  "Professionsbachelor grafisk kommunikation",
                  "Professionsbachelor it-arkitektur",
                  "Professionsbachelor jordemoder",
                  "Professionsbachelor kommunikation",
                  "Professionsbachelor kristendom kultur og kommunikation",
                  "Professionsbachelor maskinmester",
                  "Professionsbachelor medie- og sonokommunikation",
                  "Professionsbachelor medieproduktion og ledelse",
                  "Professionsbachelor natur- og kulturformidling",
                  "Professionsbachelor offentlig administration",
                  "Professionsbachelor optometri",
                  "Professionsbachelor procesøkonomi og værdikædeledelse",
                  "Professionsbachelor psykomotorik",
                  "Professionsbachelor pædagog",
                  "Professionsbachelor radiograf",
                  "Professionsbachelor skat",
                  "Professionsbachelor skibsfører",
                  "Professionsbachelor skibsofficer",
                  "Professionsbachelor skov- og landskabsingeniør",
                  "Professionsbachelor smykker teknologi og business",
                  "Professionsbachelor socialrådgiver",
                  "Professionsbachelor sygeplejerske",
                  "Professionsbachelor tandplejer",
                  "Professionsbachelor tekstildesign -håndværk og formidling",
                  "Professionsbachelor tv- og medietilrettelæggelse",
                  "Professionsbachelor urban landskabsingeniør",
                  "Professionsbachelor visuel kommunikation",
                  "Professionsbachelor økonomi og It",
                  "Psykologi",
                  "Pædagogik",
                  "Religionsstudier",
                  "Religionsvidenskab",
                  "Retorik",
                  "Ruslandstudier",
                  "Samfundsfag",
                  "Samfundsvidenskabelig bacheloruddannelse",
                  "Samfundsvidenskabelig bacheloruddannelse + journalistik + andet fag",
                  "Samfundsvidenskabelig international bacheloruddannelse",
                  "Serviceøkonom",
                  "Sociologi",
                  "Sociologi og kulturanalyse",
                  "Softwareudvikling",
                  "Spansk og spanskamerikansk sprog litteratur og kultur",
                  "Spansk sprog og internationale studier",
                  "Spansk sprog og kultur",
                  "Sprog og internationale studier engelsk",
                  "Statskundskab",
                  "Sundhed og informatik",
                  "Sundhedsadministrativ koordinator",
                  "Teater- og performancestudier",
                  "Teknisk videnskab (civilingeniør) Arkitektur og design",
                  "Teknisk videnskab (civilingeniør) Bioteknologi",
                  "Teknisk videnskab (civilingeniør) By- energi- og miljøplanlægning",
                  "Teknisk videnskab (civilingeniør) Byggeri",
                  "Teknisk videnskab (civilingeniør) Byggeri og anlæg",
                  "Teknisk videnskab (civilingeniør) Byggeteknologi",
                  "Teknisk videnskab (civilingeniør) Bygningsdesign",
                  "Teknisk videnskab (civilingeniør) Bygningsteknik",
                  "Teknisk videnskab (civilingeniør) Bæredygtigt design",
                  "Teknisk videnskab (civilingeniør) Bæredygtigt energidesign",
                  "Teknisk videnskab (civilingeniør) Computerteknologi",
                  "Teknisk videnskab (civilingeniør) Cyber- og computerteknologi",
                  "Teknisk videnskab (civilingeniør) Cyberteknologi",
                  "Teknisk videnskab (civilingeniør) Design og innovation",
                  "Teknisk videnskab (civilingeniør) Elektronik og it",
                  "Teknisk videnskab (civilingeniør) Elektroteknologi",
                  "Teknisk videnskab (civilingeniør) Energi",
                  "Teknisk videnskab (civilingeniør) Energiteknologi",
                  "Teknisk videnskab (civilingeniør) Fysik og nanoteknologi",
                  "Teknisk videnskab (civilingeniør) Fysik og teknologi",
                  "Teknisk videnskab (civilingeniør) Geofysik og Rumteknologi",
                  "Teknisk videnskab (civilingeniør) Globale forretningssystemer",
                  "Teknisk videnskab (civilingeniør) Ingeniørvidenskab",
                  "Teknisk videnskab (civilingeniør) Kemi og bioteknologi",
                  "Teknisk videnskab (civilingeniør) Kemi og teknologi",
                  "Teknisk videnskab (civilingeniør) Kemiteknologi",
                  "Teknisk videnskab (civilingeniør) Kunstig intelligens og data",
                  "Teknisk videnskab (civilingeniør) Life Science og Teknologi",
                  "Teknisk videnskab (civilingeniør) Maskinteknik",
                  "Teknisk videnskab (civilingeniør) Matematik og teknologi",
                  "Teknisk videnskab (civilingeniør) Matematik-teknologi",
                  "Teknisk videnskab (civilingeniør) Medicin og teknologi",
                  "Teknisk videnskab (civilingeniør) Mekanik",
                  "Teknisk videnskab (civilingeniør) Mekanik og produktion",
                  "Teknisk videnskab (civilingeniør) Miljøvidenskab",
                  "Teknisk videnskab (civilingeniør) Nanoteknologi",
                  "Teknisk videnskab (civilingeniør) Produkt- og designpsykologi",
                  "Teknisk videnskab (civilingeniør) Produktion og konstruktion",
                  "Teknisk videnskab (civilingeniør) Robotteknologi",
                  "Teknisk videnskab (civilingeniør) Software",
                  "Teknisk videnskab (civilingeniør) Software Engineering",
                  "Teknisk videnskab (civilingeniør) Softwareteknologi",
                  "Teknisk videnskab (civilingeniør) Spiludvikling og læringsteknologi",
                  "Teknisk videnskab (civilingeniør) Strategisk analyse og systemdesign",
                  "Teknisk videnskab (civilingeniør) Sundheds- og velfærdsteknologi",
                  "Teknisk videnskab (civilingeniør) Sundhedsteknologi",
                  "Teknisk videnskab (civilingeniør) Vand bioressourcer og miljømanagement",
                  "Teknoantropologi",
                  "Teologi",
                  "Tysk",
                  "Tysk sprog og kultur",
                  "Tysk sprog litteratur og kultur",
                  "Uddannelsesvidenskab",
                  "Veterinærmedicin",
                  "Æstetik og kultur",
                  "Økonomi",
                  "Østeuropastudie",]

    objects = [HigherEducationProgramme(name=name) for name in educations]

    db.session.bulk_save_objects(objects)
    db.session.commit()

    print("Added higher educations")


@fake.cli.command()
def customers_excell():  # pragma: no cover

    import requests
    import json
    import pandas as pd
    import time

    from decouple import config
    api_key = config("TW_API")
    headers = {
        'Authorization': f'Token token={api_key}',
        'Content-Type': 'application/json'
    }
    url1 = f"https://api.teachworks.com/v1/customers?per_page=50&page={1}"
    payload = {}
    response1 = requests.request("GET", url1, headers=headers, data=payload)
    json_response = response1.json()
    excel_all_data = pd.json_normalize(json_response)
    a = range(0, 53)
    for i in a:
        time.sleep(1)
        i_request = i+1
        url = f"https://api.teachworks.com/v1/customers?per_page=50&page={i_request}"
        response = requests.request("GET", url, headers=headers, data=payload)
        json_response = response.json()
        print(response)
        read_js = pd.json_normalize(json_response)
        excel_all_data = excel_all_data.append(read_js, ignore_index=True)
        print(excel_all_data)

    excell = excel_all_data.to_excel(f'customers_all.xlsx')


@fake.cli.command()
def saveCustomers():
    import pandas as pd
    customers = pd.read_excel('customers_all.xlsx')
    dict_customers = customers.to_dict()
    # Customer.add_customer_user()
    for i in range(0, len(dict_customers['id'])):
        status = dict_customers['status'][i].lower()
        if dict_customers['status'][i].lower() != 'prospective':
            phone = dict_customers['mobile_phone'][i] or ""
            if type(phone) == str:
                if not phone.startswith("+"):
                    phone = "+45" + phone
            else:
                phone = '+453214'
            if type(dict_customers['email'][i]) == str:
                check_user = User.query.filter_by(
                    email=dict_customers['email'][i].lower()).first()
                if check_user is None:
                    user = User(first_name=dict_customers['first_name'][i],
                                last_name=dict_customers['last_name'][i],
                                email=dict_customers['email'][i].lower(),
                                phone=phone,
                                password=''
                                )
                    db.session.add(user)
                    db.session.commit()
                    if dict_customers['email_lesson_reminders'][i] == 0:
                        email_lesson_reminders = False
                    else:
                        email_lesson_reminders = True
                    if dict_customers['email_lesson_notes'][i] == 0:
                        email_lesson_notes = False
                    else:
                        email_lesson_notes = True

                    customer_type = dict_customers['customer_type'][i]
                    if customer_type == 'individual':
                        customer_type = 'independent'

                    stripe_id = dict_customers['stripe_id'][i]
                    if dict_customers['stripe_id'][i] == 'NaN':
                        stripe_id = ''
                    customer = Customer(id=dict_customers['id'][i],
                                        user_id=user.uid,
                                        stripe_id=stripe_id,
                                        customer_type=customer_type,
                                        email_lesson_reminder=email_lesson_reminders,
                                        email_lesson_notes=email_lesson_notes,
                                        status=status,
                                        created_at=dict_customers['created_at'][i],
                                        last_updated=dict_customers['updated_at'][i],
                                        )
                    db.session.add(customer)
                    db.session.commit()
                    balance = Balance(customer_id=dict_customers['id'][i],
                                      hours_scheduled=0,
                                      hours_used=0,
                                      hours_free=0,
                                      hours_ordered=0,
                                      invoice_balance=0,
                                      currency='DKK')
                    db.session.add(balance)
                    db.session.commit()
                else:
                    print(f'Duplicate email{i}')
            else:
                print(f'No email provided{i}')


@fake.cli.command()
def students():

    import requests
    import json
    import pandas as pd
    import time

    from decouple import config
    api_key = config("TW_API")
    headers = {
        'Authorization': f'Token token={api_key}',
        'Content-Type': 'application/json'
    }
    url1 = f"https://api.teachworks.com/v1/students?per_page=50&page={1}"
    payload = {}
    response1 = requests.request("GET", url1, headers=headers, data=payload)
    json_response = response1.json()
    excel_all_data = pd.json_normalize(json_response)
    a = range(0, 55)
    for i in a:
        time.sleep(1)
        i_request = i+1
        url = f"https://api.teachworks.com/v1/students?per_page=50&page={i_request}"
        response = requests.request("GET", url, headers=headers, data=payload)
        json_response = response.json()
        print(response)
        read_js = pd.json_normalize(json_response)
        excel_all_data = excel_all_data.append(read_js, ignore_index=True)
        print(excel_all_data)
    excell = excel_all_data.drop_duplicates('id')
    excell = excell.to_excel(f'students_all.xlsx')


@fake.cli.command()
def saveStudents():
    import pandas as pd
    students = pd.read_excel('students_all.xlsx')
    dict_students = students.to_dict()
    for i in range(0, len(dict_students['id'])):
        if dict_students['status'][i].lower() != 'prospective':
            customer = Customer.query.filter_by(
                id=dict_students['customer_id'][i]).first()
            if customer is not None:
                if dict_students['email_lesson_reminders'][i] == 0:
                    email_lesson_reminders = False
                else:
                    email_lesson_reminders = True
                if dict_students['email_lesson_notes'][i] == 0:
                    email_lesson_notes = False
                else:
                    email_lesson_notes = True
                if dict_students['student_type'][i] == 'individual':
                    # independent customer
                    student_type = 'independent'
                    student = Student(id=dict_students['id'][i],
                                      customer_id=dict_students['customer_id'][i],
                                      status=dict_students['status'][i].lower(
                    ),
                        first_name=dict_students['first_name'][i],
                        last_name=dict_students['last_name'][i],
                        email=dict_students['email'][i].lower(),
                        email_lesson_notes=email_lesson_notes,
                        email_lesson_reminder=email_lesson_reminders,
                        created_at=dict_students['created_at'][i],
                        last_updated=dict_students['updated_at'][i],
                        student_type=student_type,
                    )
                    db.session.add(student)
                    db.session.commit()
                else:
                    if type(dict_students['email'][i]) == str:
                        # create a new User
                        check_user = User.query.filter_by(
                            email=dict_students['email'][i].lower()).first()
                        if check_user is None:
                            phone = dict_students['mobile_phone'][i] or ""
                            if type(phone) == str:
                                if not phone.startswith("+"):
                                    phone = "+45" + phone
                            else:
                                phone = '+453214'
                            user = User(first_name=dict_students['first_name'][i],
                                        last_name=dict_students['last_name'][i],
                                        email=dict_students['email'][i].lower(
                            ),
                                phone=phone,
                                password=''
                            )
                            db.session.add(user)
                            db.session.commit()
                            student_type = 'independent'
                            student = Student(id=dict_students['id'][i],
                                              customer_id=dict_students['customer_id'][i],
                                              user_id=user.uid,
                                              status=dict_students['status'][i].lower(
                            ),
                                first_name=dict_students['first_name'][i],
                                last_name=dict_students['last_name'][i],
                                created_at=dict_students['created_at'][i],
                                last_updated=dict_students['updated_at'][i],
                                email=dict_students['email'][i].lower(
                            ),
                                email_lesson_notes=email_lesson_notes,
                                email_lesson_reminder=email_lesson_reminders,
                                student_type=student_type,
                            )
                            db.session.add(student)
                            db.session.commit()
                    else:
                        customer_email = Customer.query.filter_by(
                            id=dict_students['customer_id'][i]).first()
                        student_type = 'child'
                        student = Student(id=dict_students['id'][i],
                                          customer_id=dict_students['customer_id'][i],
                                          status=dict_students['status'][i].lower(
                        ),
                            first_name=dict_students['first_name'][i],
                            last_name=dict_students['last_name'][i],
                            created_at=dict_students['created_at'][i],
                            last_updated=dict_students['updated_at'][i],
                            email=customer_email.user.email.lower(),
                            email_lesson_notes=email_lesson_notes,
                            email_lesson_reminder=email_lesson_reminders,
                            student_type=student_type,
                        )
                        db.session.add(student)
                        db.session.commit()
                        # just create a student
            else:
                print(f'Email duplicated {i}')


@fake.cli.command()
def connectTeachersStudents():
    import pandas as pd
    import time
    import requests
    students = pd.read_excel('students_all.xlsx')
    import ast
    from decouple import config
    api_key = config("TW_API")
    headers = {
        'Authorization': f'Token token={api_key}',
        'Content-Type': 'application/json'
    }
    dict_students = students.to_dict()
    for i in range(0, len(dict_students['id'])):
        if dict_students['status'][i].lower() != 'prospective':
            tutor_id = dict_students['default_teachers'][i]
            tutor_list = ast.literal_eval(tutor_id)
            student = Student.query.filter_by(
                id=dict_students['id'][i]).first()
            if student is not None:

                for i in tutor_list:
                    id = i['id']
                    url1 = f"https://api.teachworks.com/v1/employees/{id}"
                    payload = {}
                    time.sleep(1)
                    response1 = requests.request(
                        "GET", url1, headers=headers, data=payload)
                    json_response = response1.json()
                    print(json_response['email'].lower())
                    user = User.query.filter_by(
                        email=json_response['email'].lower()).first()
                    print(user.teacher)
                    student.teachers.append(user.teacher)
            db.session.commit()


@fake.cli.command()
def lessons():
    import requests
    import json
    import pandas as pd
    import time

    from decouple import config
    api_key = config("TW_API")
    headers = {
        'Authorization': f'Token token={api_key}',
        'Content-Type': 'application/json'
    }
    url1 = f"https://api.teachworks.com/v1/lessons?per_page=50&page={1}"
    payload = {}
    response1 = requests.request("GET", url1, headers=headers, data=payload)
    json_response = response1.json()
    excel_all_data = pd.json_normalize(json_response)
    a = range(1, 204)
    for i in a:
        time.sleep(1)
        i_request = i+1
        url = f"https://api.teachworks.com/v1/lessons?per_page=50&page={i_request}"
        response = requests.request("GET", url, headers=headers, data=payload)
        json_response = response.json()
        print(response)
        read_js = pd.json_normalize(json_response)
        excel_all_data = excel_all_data.append(read_js, ignore_index=True)
        print(excel_all_data)
    excell = excel_all_data.to_excel(f'lessons_all.xlsx')


@fake.cli.command()
def saveLessons():
    import pandas as pd
    import time
    import requests
    lessons = pd.read_excel('lessons_all.xlsx')
    import ast
    from decouple import config

    dict_lessons = lessons.to_dict()
    for i in range(0, len(dict_lessons['id'])):
        employee_id = dict_lessons['employee_id'][i]

        teacher = Teacher.query.filter_by(teachworks=str(employee_id)).first()
        if teacher is not None:
            teacher_id = teacher.id
            id = dict_lessons['id'][i]
            from_time = dict_lessons['from_datetime'][i]
            to_time = dict_lessons['to_datetime'][i]
            duration_in_minutes = dict_lessons['duration_minutes'][i]
            created_at = dict_lessons['created_at'][i]
            completed_at = dict_lessons['completed_at'][i]
            if type(completed_at) != str:
                completed_at = datetime.datetime.utcnow()
            updated_at = dict_lessons['updated_at'][i]
            wage = dict_lessons['wage'][i]
            status = dict_lessons['status'][i].lower()
            if status == 'cancelled':
                if type(dict_lessons['custom_status'][i]) == str:
                    if dict_lessons['custom_status'][i] == 'Rettidig aflysning (før kl. 9:00)':
                        status = 'good cancellation'
                    elif dict_lessons['custom_status'][i] == 'Tutor aflyste for sent (efter kl. 9:00)':
                        status = 'bad cancellation teacher'
                    else:
                        status = 'bad cancellation teacher'
                else:
                    status = 'bad cancellation teacher'
            elif status == 'missed':
                status = 'bad cancellation student'
            trial_lesson = False
            title = ''
            completion_notes = ''
            if dict_lessons['service_name'][i] == 'Opstartstid' \
                    or dict_lessons['service_name'][i] == 'Opstartstid (universitetsniveau)' \
                    or dict_lessons['service_name'][i] == 'Opstartsmøde':
                trial_lesson = True
            student_data = ast.literal_eval(dict_lessons['participants'][i])
            for j in student_data:
                student_id = j['student_id']
                student = Student.query.get(student_id)
                if student is not None:
                    title = f'Lesson with {student.first_name} {student.last_name}'
                    completion_notes = j['public_notes']
                    if completion_notes is None:
                        completion_notes = ''
                    lesson_reminder_sent_at = j['student_reminder_sent_at']
                    if lesson_reminder_sent_at is None:
                        lesson_reminder_sent_at = datetime.datetime.utcnow()
            paid = False
            wage_id = dict_lessons['wage_payment_id'][i]
            if isinstance(wage_id, (int, float, complex)):
                paid = True
            check_id = Lesson.query.filter_by(id=id).first()
            if check_id is None:
                lesson = Lesson(id=id, teacher_id=teacher_id,
                                title=title,
                                description='',
                                completion_notes=completion_notes,
                                lesson_reminder_sent_at=lesson_reminder_sent_at,
                                status=status,
                                trial_lesson=trial_lesson,
                                created_at=created_at,
                                last_updated=updated_at,
                                completed_at=completed_at,
                                wage=wage,
                                duration_in_minutes=duration_in_minutes,
                                from_time=from_time,
                                to_time=to_time,
                                space='',
                                space_id='',
                                secret='',
                                session_id='',
                                paid=paid)
                db.session.add(lesson)
                db.session.commit()
                for j in student_data:
                    student = Student.query.get(j['student_id'])
                    if student is not None:
                        lesson.lessons_students.append(student)
                        db.session.commit()
            else:
                print(f'duplicated lesson {id}')


@fake.cli.command()
def wagepayments():
    import requests
    import json
    import pandas as pd
    import time

    from decouple import config
    api_key = config("TW_API")
    headers = {
        'Content-Type': 'application/json'
    }
    url1 = f"https://api.teachworks.com/v1/wage_payments?per_page=50&page={1}"
    url_copensation = f"https://api.teachworks.com/v1/other_compensation?per_page=50&page={1}"
    payload = {}
    response1 = requests.request("GET", url1, headers=headers, data=payload)
    response_compensation = requests.request(
        "GET", url_copensation, headers=headers, data=payload)
    json_response = response1.json()
    json_compensation = response_compensation.json()
    excel_all_data = pd.json_normalize(json_response)
    other_comp_excell = pd.json_normalize(json_compensation)
    a = range(1, 35)
    b = range(1, 4)
    for i in a:
        time.sleep(1)
        i_request = i+1
        url = f"https://api.teachworks.com/v1/wage_payments?per_page=50&page={i_request}"
        response = requests.request("GET", url, headers=headers, data=payload)
        json_response = response.json()
        print(response)
        read_js = pd.json_normalize(json_response)
        excel_all_data = excel_all_data.append(read_js, ignore_index=True)
        print(excel_all_data)

    for j in b:
        time.sleep(1)
        i_request = j+1
        url = f"https://api.teachworks.com/v1/other_compensation?per_page=50&page={i_request}"
        response = requests.request("GET", url, headers=headers, data=payload)
        json_response = response.json()
        print(response)
        read_js = pd.json_normalize(json_response)
        other_comp_excell = other_comp_excell.append(
            read_js, ignore_index=True)
        print(other_comp_excell)
    other_comp_excell.to_excel(f'other_compensation_all.xlsx')
    excell = excel_all_data.to_excel(f'wage_payments_all.xlsx')


@fake.cli.command()
def saveWages():
    import pandas as pd
    import time
    import requests
    wage_payments = pd.read_excel('wage_payments_all.xlsx')
    lessons = pd.read_excel('lessons_all.xlsx')

    import ast
    import math
    from decouple import config
    dict_lessons = lessons.to_dict()
    dict_wages = wage_payments.to_dict()
    for i in range(0, len(dict_wages['id'])):
        teacher_id = dict_wages['employee_id'][i]
        teacher = Teacher.query.filter_by(teachworks=str(teacher_id)).first()
        if teacher is not None:
            hours = 0
            for j in range(0, len(dict_lessons['id'])):
                if isinstance(dict_lessons['wage_payment_id'][j], (int, float, complex)):
                    if dict_wages['id'][i] == dict_lessons['wage_payment_id'][j]:
                        hours += dict_lessons['duration_minutes'][i]
            payment_date = datetime.datetime.strptime(
                dict_wages['sent_at'][i], "%Y-%m-%dT%H:%M:%S.000Z")
            from_date = payment_date + relativedelta(months=-1)
            from_date = payment_date.replace(
                day=16, hour=0, minute=0, second=0)
            to_date = payment_date.replace(
                day=15, hour=23, minute=59, second=59)
            wagepayment = WagePayment(id=dict_wages['id'][i],
                                      teacher_id=teacher.id,
                                      amount=dict_wages['amount'][i],
                                      hours=round(hours/60, 2),
                                      payment_date=payment_date,
                                      from_date=from_date,
                                      to_date=to_date,
                                      created_at=dict_wages['created_at'][i],
                                      last_updated=dict_wages['updated_at'][i],
                                      referrals_amount=0,
                                      referrals_number=0
                                      )
            db.session.add(wagepayment)
            db.session.commit()
    referrals_data = pd.read_excel('other_compensation_all.xlsx')
    dict_referrals = referrals_data.to_dict()
    for i in range(0, len(dict_referrals['id'])):
        wagepayment = WagePayment.query.filter_by(
            id=dict_referrals['wage_payment_id'][i]).first()
        if wagepayment is not None:
            teacher = Teacher.query.filter_by(teachworks=str(
                dict_referrals['employee_id'][i])).first()
            if teacher is not None:
                wagepayment.referrals_amount = dict_referrals['amount'][i]
                wagepayment.referrals_number = dict_referrals['amount'][i]/200
                referral = Referral(id=dict_referrals['id'][i],
                                    referrer_id=teacher.id,
                                    referred_id=1,
                                    paid=True,
                                    created_at=dict_referrals['created_at'][i],
                                    last_updated=dict_referrals['updated_at'][i],
                                    wage_payment_id=wagepayment.id,
                                    referral_amount=dict_referrals['amount'][i]
                                    )
                db.session.add(referral)
                db.session.commit()


@fake.cli.command()
def orders():
    import pandas as pd
    import time
    import requests
    from decouple import config
    api_key = config("TW_API")
    headers = {
        'Authorization': f'Token token={api_key}',
        'Content-Type': 'application/json'
    }
    url1 = f"https://api.teachworks.com/v1/invoices?per_page=50&page=1"
    payload = {}
    response1 = requests.request("GET", url1, headers=headers, data=payload)
    json_response = response1.json()
    excel_all_data = pd.json_normalize(json_response)
    a = range(1, 60)
    for i in a:
        time.sleep(1)
        i_request = i+1
        url = f"https://api.teachworks.com/v1/invoices?per_page=50&page={i_request}"
        response = requests.request("GET", url, headers=headers, data=payload)
        json_response = response.json()
        print(response)
        read_js = pd.json_normalize(json_response)
        excel_all_data = excel_all_data.append(read_js, ignore_index=True)
        print(excel_all_data)
    excel_all_data.to_excel('invoices_all.xlsx')


@fake.cli.command()
def saveOrders():
    import pandas as pd
    import time
    import requests
    import ast
    import math
    from decouple import config
    import hashlib
    data_orders = pd.read_excel('invoices_all.xlsx')
    dict_orders = data_orders.to_dict()
    for i in range(0, len(dict_orders['id'])):
        customer = Customer.query.filter_by(
            id=dict_orders['customer_id'][i]).first()
        if int(dict_orders['total'][i]) != 0:
            if customer is not None:
                id = dict_orders['id'][i]
                uid_hash = str(id) + str("")
                uid_hash = uid_hash.encode('utf-8')
                hashed_id = hashlib.sha224(uid_hash).hexdigest()

                stripe_customer_id = ''
                active = False
                if customer.stripe_id != '':
                    stripe_customer_id = customer.stripe_id
                status = dict_orders['status'][i].lower()
                if status == 'approved':
                    status = 'pending'
                    active = True
                elif status == 'saved':
                    status = 'paid'
                package_data = ast.literal_eval(dict_orders['packages'][i])
                unit_price = 0
                discount = ''
                total_hours = 0
                package = ''
                installments = 0
                expiration_date = datetime.datetime.strptime(
                    dict_orders['created_at'][i], "%Y-%m-%dT%H:%M:%S.000Z")
                for j in package_data:
                    total_hours = float(j['quantity'])
                    unit_price = float(j['unit_price'])
                    if j['discount_rate'] is not None:
                        discount = int(float(j['discount_rate']))
                        converted = int(unit_price)
                        if discount == 0:
                            discount = ''
                        if converted == 399:
                            installments = 3
                            expiration_date = expiration_date + \
                                relativedelta(months=+3)
                        elif converted == 309:
                            installments = 6
                            expiration_date = expiration_date + \
                                relativedelta(months=+6)
                        elif converted == 289:
                            installments = 12
                            expiration_date = expiration_date + \
                                relativedelta(months=+12)
                        elif converted == 269:
                            installments = 18
                            expiration_date = expiration_date + \
                                relativedelta(months=+18)
                        elif converted == 249:
                            installments = 24
                            expiration_date = expiration_date + \
                                relativedelta(months=+24)
                        elif converted == 229:
                            installments = 36
                            expiration_date = expiration_date + \
                                relativedelta(months=+36)
                        else:
                            installments = 3
                            expiration_date = expiration_date + \
                                relativedelta(months=+3)
                        package = f'{installments}-months-{converted}'
                    order = Order(
                        teachworks_id=id,
                        hashed_id=hashed_id,
                        customer_id=customer.id,
                        balance_id=customer.balance[0].id,
                        package=package,
                        installments=installments,
                        total_hours=total_hours,
                        total_price=unit_price*total_hours,
                        unit_price=unit_price,
                        crm_deal_id='',
                        discount=discount,
                        status=status,
                        stripe_customer_id=stripe_customer_id,
                        stripe_url=f'toptutors.dk/order/{hashed_id}',
                        created_at=dict_orders['created_at'][i],
                        last_updated=dict_orders['updated_at'][i],
                        booking_date=dict_orders['created_at'][i],
                        expiration_date=expiration_date,
                        active=active,
                        email_sent=True,
                        upsell=False
                    )
                    if status == 'void':
                        order.void_date = dict_orders['updated_at'][i]
                    db.session.add(order)
                    db.session.commit()
            else:
                cust = dict_orders['customer_id'][i]
                print(f'Customer does not exist {cust}')
    orders = Order.query.all()
    for i in orders:
        if i.unit_price == 0:
            i.balance.hours_free = i.balance.hours_free+i.total_hours
        elif i.status.value != 'void':
            i.balance.hours_ordered = i.balance.hours_ordered+i.total_hours
            i.balance.invoice_balance = i.balance.invoice_balance-i.total_price
            db.session.commit()


@fake.cli.command()
def addPayments():
    import pandas as pd
    import time
    import requests
    transactions_stripe = pd.read_csv('payments.csv')
    import ast
    import math
    from decouple import config
    all_missing = set()
    white_list = {'sophia.fugleholm@yahoo.com', "kvittering@loyaltykey.com", "almagrill@gmail.com",
                  "elias.wahib@hotmail.com", "michael@evander.dk", "signeskovnielsen@icloud.com",
                  "laerkehygom@gmail.com",
                  "michaelmcfly75@gmail.com", "zain01591998@gmail.com",
                  "usma.qureshi@gmail.com", "thh@el-salg.dk",
                  "yassercph@icloud.com", "riisagermerete@gmail.com",
                  "bobbekaer@gmail.com", "sgulercelik@gmail.com", "elmar@toptutors.dk",
                  "sundus11@live.dk", "linewp@outlook.dk", "gamzecelik0114@gmail.com",
                  "eastduck@gmail.com", "yasmin070905@gmail.com", "larsenkamille05@gmail.com",
                  "rasmuskuszon@gmail.com", "walid.maaijil@hotmail.com", "sabir.ayub@hotmail.com",
                  "fesinkoroglu@gmail.com", "carina.scharling@gmail.com", "mghannam21@gmail.com",
                  "laurabruun8@gmail.com", "astrid.caroline2@gmail.com"
                  }
    dict_transactions = transactions_stripe.to_dict()
    for i in range(0, len(dict_transactions['id'])):
        if dict_transactions['Customer Email'][i].lower() not in white_list:
            try:
                amount = float(
                    dict_transactions['Amount'][i].replace(',', '.'))
            except:
                amount = float(
                    int(dict_transactions['Amount'][i]).replace(',', '.'))

            user = User.query.filter_by(
                email=dict_transactions['Customer Email'][i].lower()).first()
            if user is not None:
                if user.customer is not None:
                    transaction = Transaction(
                        type_transaction='payment',
                        customer_id=user.customer.id,
                        balance_id=user.customer.balance[0].id,
                        currency='DKK',
                        amount=amount,
                        created_at=dict_transactions['Created (UTC)'][i],
                        method='stripe',
                        stripe_transaction_id=dict_transactions['id'][i]
                    )
                    db.session.add(transaction)
                    db.session.commit()
                elif user.is_student:
                    transaction = Transaction(
                        type_transaction='payment',
                        customer_id=user.student.customer.id,
                        balance_id=user.student.customer.balance[0].id,
                        currency='DKK',
                        amount=amount,
                        created_at=dict_transactions['Created (UTC)'][i],
                        method='stripe',
                        stripe_transaction_id=dict_transactions['id'][i]
                    )
                    db.session.add(transaction)
                    db.session.commit()
                else:
                    user_duplicate = User.query.filter_by(
                        email=f'{user.email}.duplicate').first()
                    if user_duplicate is not None:
                        transaction = Transaction(
                            type_transaction='payment',
                            customer_id=user_duplicate.customer.id,
                            balance_id=user_duplicate.customer.balance[0].id,
                            currency='DKK',
                            amount=amount,
                            created_at=dict_transactions['Created (UTC)'][i],
                            method='stripe',
                            stripe_transaction_id=dict_transactions['id'][i]
                        )
                        db.session.add(transaction)
                        db.session.commit()
            else:
                all_missing.add(dict_transactions['Customer Email'][i])

    transactions_stripe_refunds = pd.read_csv('refunds.csv')
    import ast
    import math
    dict_transactions_refunds = transactions_stripe_refunds.to_dict()
    for i in range(0, len(dict_transactions_refunds['id'])):
        if dict_transactions_refunds['Customer Email'][i].lower() not in white_list:
            try:
                amount = float(
                    dict_transactions_refunds['Amount Refunded'][i].replace(',', '.'))
            except:
                amount = float(
                    int(dict_transactions_refunds['Amount Refunded'][i]).replace(',', '.'))
            user = User.query.filter_by(
                email=dict_transactions_refunds['Customer Email'][i].lower()).first()
            if user is not None:
                if user.customer is not None:
                    transaction = Transaction(
                        type_transaction='refund',
                        customer_id=user.customer.id,
                        balance_id=user.customer.balance[0].id,
                        currency='DKK',
                        amount=amount,
                        created_at=dict_transactions_refunds['Created (UTC)'][i],
                        method='stripe',
                        stripe_transaction_id=dict_transactions_refunds['id'][i]
                    )
                    db.session.add(transaction)
                    db.session.commit()
                elif user.is_student:
                    transaction = Transaction(
                        type_transaction='refund',
                        customer_id=user.student.customer.id,
                        balance_id=user.student.customer.balance[0].id,
                        currency='DKK',
                        amount=amount,
                        created_at=dict_transactions_refunds['Created (UTC)'][i],
                        method='stripe',
                        stripe_transaction_id=dict_transactions_refunds['id'][i]
                    )
                    db.session.add(transaction)
                    db.session.commit()
                else:
                    user_duplicate = User.query.filter_by(
                        email=f'{user.email}.duplicate').first()
                    if user_duplicate is not None:
                        transaction = Transaction(
                            type_transaction='refund',
                            customer_id=user_duplicate.customer.id,
                            balance_id=user_duplicate.customer.balance[0].id,
                            currency='DKK',
                            amount=amount,
                            created_at=dict_transactions_refunds['Created (UTC)'][i],
                            method='stripe',
                            stripe_transaction_id=dict_transactions_refunds['id'][i]
                        )
                        db.session.add(transaction)
                        db.session.commit()
            else:
                all_missing.add(dict_transactions_refunds['Customer Email'][i])
    print(all_missing)
    transactions = Transaction.query.all()
    for i in transactions:
        if i.type_transaction.value == 'payment':
            i.balance.invoice_balance += round(i.amount, 2)
        else:
            i.balance.invoice_balance -= round(i.amount, 2)
        db.session.commit()


@fake.cli.command()
def lessonhours():
    lessons = Lesson.query.all()
    date_last = datetime.datetime(2023, 1, 1, 0, 0, 1)
    for i in lessons:
        duration = round(i.duration_in_minutes/60, 2)
        for j in i.lessons_students:
            if not i.trial_lesson:
                if j.customer is not None:
                    if i.status.value == 'scheduled':
                        j.customer.balance[0].hours_scheduled += duration
                    elif i.status.value == 'attended':
                        j.customer.balance[0].hours_used += duration
                    elif i.status.value == 'bad cancellation student':
                        print('cancelled')
                        if duration > 2:
                            j.customer.balance[0].hours_used += 2
                        else:
                            j.customer.balance[0].hours_used += duration
            if i.created_at >= date_last:
                lesson_url = create_lesson_space(i.lessons_teacher, j)
                i.space_id = lesson_url['room_id']
                i.secret = lesson_url['secret']
                i.session_id = lesson_url['session_id']
                i.space = lesson_url['space']
    db.session.commit()


@fake.cli.command()
def cleanup():
    # users= User.query.filter(User.uid >5641).all()
    # print(users)
    # for i in users:
    #    db.session.delete(i)
    #    db.session.commit()
    import stripe
    from decouple import config
    import ast
    import pandas as pd
    import pandas as pd
    import time
    import requests
    import ast
    from sqlalchemy.orm import joinedload
    from decouple import config
    lessons_all = pd.read_excel('lessons_all.xlsx')
    lessons = Lesson.query.options(joinedload(Lesson.lessons_students)).all()
    for i in lessons:
        if len(i.lessons_students) == 0:
            searched_lesson = lessons_all.loc[lessons_all['id'] == i.id]
            for j in searched_lesson['participants']:
                converted = ast.literal_eval(j)
                for m in converted:
                    student = Student.query.get(m['student_id'])
                    if student is None:
                        print(i.id)
                    else:
                        i.lessons_students.append(student)
                        i.title = f'Lesson with {student.first_name} {student.last_name}'
                        i.completion_notes = m['public_notes']
    db.session.commit()
    student = Customer.query.get(1155899)
    print(student)
    debug_time = Lesson.query.all()
    for i in debug_time:
        i.created_at
        i.last_updated


@fake.cli.command()
def confirm_balances():
    import stripe
    from decouple import config
    import ast
    import pandas as pd
    import pandas as pd
    import time
    import requests
    import ast
    data_teachers = pd.read_excel('CustomerBalances.xlsx')
    dict_teachers = data_teachers.to_dict()
    api_key = config("TW_API")
    headers = {
        'Authorization': f'Token token={api_key}',
        'Content-Type': 'application/json'
    }
    payload = {}
    for i in range(0, len(dict_teachers['First Name'])):
        first_name = dict_teachers['First Name'][i]
        last_name = dict_teachers['Last Name'][i]
        time.sleep(1)
        url = f"https://api.teachworks.com/v1/customers?per_page=50&first_name={first_name}&last_name={last_name}&status=Active"
        response = requests.request("GET", url, headers=headers, data=payload)
        json_response = response.json()
        read_js = pd.json_normalize(json_response)
        for j in read_js['id']:
            customer = Customer.query.get(j)
            if customer is not None:
                if abs(customer.balance[0].invoice_balance) != dict_teachers['Balance'][i]:
                    print(f"Incorrect balance for {j}")
                    print(customer.balance[0].invoice_balance,
                          dict_teachers['Balance'][i])


@fake.cli.command()
def create_user_csv():

    import pandas as pd
    import numpy as np
    users = User.query.all()

    def get_uid_for_request(i):
        if i.is_customer:
            return i.customer.id
        elif i.is_student:
            return i.student.id
        elif i.is_teacher:
            return i.teacher.id
    users_for_csv = [(i.email, i.uid, "", i.get_roles[0],
                      get_uid_for_request(i)) for i in users]
    arr = np.asarray(users_for_csv)
    df = pd.DataFrame(arr)
    df = df.reindex(np.random.permutation(df.index))
    df.to_csv('users_for_testing.csv', header=[
              'EMAIL', 'ID', 'PASSWORD', 'TYPE_USER', 'USER_TYPE_ID'])


@fake.cli.command()
def saveTeachers():
    import requests
    import json
    import pandas as pd
    import numpy as np
    import time

    from decouple import config
    api_key = config("TW_API")
    headers = {
        'Authorization': f'Token token={api_key}',
        'Content-Type': 'application/json'
    }
    url1 = f"https://api.teachworks.com/v1/employees?per_page=50&page={1}"
    payload = {}
    response1 = requests.request("GET", url1, headers=headers, data=payload)
    json_response = response1.json()
    excel_all_data = pd.json_normalize(json_response)
    a = range(0, 30)
    for i in a:
        time.sleep(1)
        i_request = i+1
        url = f"https://api.teachworks.com/v1/employees?per_page=50&page={i_request}"
        response = requests.request("GET", url, headers=headers, data=payload)
        json_response = response.json()
        read_js = pd.json_normalize(json_response)
        excel_all_data = excel_all_data.append(read_js, ignore_index=True)
    new = excel_all_data.filter(['id', 'custom_fields'], axis=1)
    test = pd.DataFrame()
    for i in range(0, len(new['id'])):
        temp_df = pd.DataFrame()
        for j in new['custom_fields'][i]:
            a = list()
            value = ' '
            if j['value'] is not None:
                value = j['value']
            a.append(value)
            temp_df[j['name']] = a
        print(temp_df)
        test = test.append(temp_df, ignore_index=True)
    new = new.merge(test, right_index=True, left_index=True)
    print(new)
    excel_all_data = excel_all_data.merge(
        new, right_index=True, left_index=True)
    excell = excel_all_data.to_excel(f'teachers_all.xlsx')


@fake.cli.command()
def teachersapi():
    import pandas as pd
    data_teachers = pd.read_excel('teachers_all.xlsx')
    dict_teachers = data_teachers.to_dict()
    for i in range(0, len(dict_teachers['id_x'])):
        teacher_check = Teacher.query.get(dict_teachers['id_x'][i])
        if teacher_check is None:
            first_name = dict_teachers["first_name"][i]
            last_name = dict_teachers["last_name"][i]
            email = ''
            if type(dict_teachers["email"][i]) == str:
                email = dict_teachers["email"][i].lower()
            # Remove spaces in phone number
            phone = ''
            if type(dict_teachers["mobile_phone"][i]) == str:
                phone = dict_teachers["mobile_phone"][i].replace(
                    " ", "").replace("(", "").replace(")", "")

                if not phone.startswith("+"):
                    phone = "+45" + phone
                if len(phone) != 11:
                    print("ERROR: PHONE NOT 11 CHARS.", phone)
                    print("Tutor:", first_name, last_name)

            open_for_new_students = True
            if dict_teachers["Vil du have flere forløb?"][i] == "Jeg vil ikke have flere forløb i øjeblikket":
                open_for_new_students = False
            payroll_id = ''
            if type(dict_teachers["CPR-nr (DDMMÅÅ-XXXX)"][i]) == str:
                payroll_id = dict_teachers["CPR-nr (DDMMÅÅ-XXXX)"][i].replace(
                    "-", "")
                local_store = payroll_id[0:6]+"-"+payroll_id[6:]
                payroll_id = local_store
            print(payroll_id)
            # Only get the digits
            reg_and_bank_digits = ''
            if type(dict_teachers["Reg nr. og konto nr. (f.eks. XXXX-XXXXXXXXXX)"][i]) == str:
                reg_and_bank_digits = ''.join(
                    char for char in dict_teachers["Reg nr. og konto nr. (f.eks. XXXX-XXXXXXXXXX)"][i] if char.isdigit())

                # the first 4 digits is the reg number and the rest is bank number
                reg_number = reg_and_bank_digits[:4]

                # The rest after the reg number
                bank_number = reg_and_bank_digits[4:]

            finished_highschool = False
            if dict_teachers["Går du stadig på gymnasiet eller ej? "][i] == "Jeg er færdig med gymnasiet":
                finished_highschool = True
            photo = ''
            if dict_teachers['photo'][i] is not None:
                photo = dict_teachers['photo'][i]

            string_to_value_mapping = {
                "7 til 8": 7,
                "8 til 9": 8,
                "9 til 10": 9,
                "10 til 11": 10,
                "11 til 12": 11,
                "Over 12": 12,
            }

            grade_average = string_to_value_mapping.get(
                dict_teachers["Karaktergennemsnit"][i], 0)

            genders = {
                "Mand": "male",
                "Kvinde": "female"
            }
            gender = genders.get(dict_teachers["Køn"][i])

            # If empty string then make it Null
            birthday = dict_teachers["birth_date"][i]
            print(birthday, type(birthday), "birthday before")
            if birthday == "":
                birthday = None

            if pd.isna(birthday):
                birthday = None

            print(birthday, type(birthday), "birthday after")

            user = User(
                email=email,
                password="",
                first_name=first_name,
                last_name=last_name,
                phone=phone
            )

            db.session.add(user)
            db.session.commit()

            teacher = Teacher(
                id=dict_teachers["id_x"][i],
                user_id=user.uid,
                wage_per_hour=150,
                bio=dict_teachers["bio"][i],
                status=dict_teachers["status"][i].lower(),
                country=dict_teachers["country"][i] or "Denmark",
                address=dict_teachers["address"][i],
                city=dict_teachers["city"][i],
                zip_code=dict_teachers["zip"][i],
                gender=gender,
                photo=photo,
                created_on_tw_at=dict_teachers["created_at"][i],
                updated_on_tw_at=dict_teachers["updated_at"][i],
                created_at=dict_teachers["created_at"][i],
                last_updated=dict_teachers["updated_at"][i],
                open_for_new_students=open_for_new_students,
                birthday=birthday,
                bank_number=bank_number,
                reg_number=reg_number,
                teachworks=dict_teachers["id_x"][i],
                payroll_id=payroll_id,
                grade_average=grade_average,
                internal_note=dict_teachers["Intern note"][i],
                how_they_found=dict_teachers["Hvor har du hørt om os? "][i],
                finished_highschool=finished_highschool,
                inactive_reason=dict_teachers["Grund til tutor stopper "][i],
                application_reason=dict_teachers["Hvorfor valgte du at ansøge hos TopTutors?"][i],
            )

            # SUBJECTS
            subjects = ''
            # Get the string of comma seperated subjects
            if type(dict_teachers["subjects"][i]) == str:
                subjects = dict_teachers["subjects"][i]
            # Split the comma-separated string into a list of subject names
            subject_names = list(set([name.strip()
                                      for name in subjects.split(',') if name.strip()]))
            subjects = []
            for name in subject_names:
                subject = Subjects.query.filter_by(name=name).first()
                if not subject:
                    raise NameError("SUBJECT NAME DOES NOT EXIST ", name)
                subjects.append(subject)

            # Assign the Subject instances to the Teacher instance
            teacher.subjects = subjects

            # PROGRAMS
            programs = ''
            # Get the string of comma seperated programs
            if type(dict_teachers["Programmer du kan anvende"][i]) == str:
                programs = dict_teachers["Programmer du kan anvende"][i]
            # Split the comma-separated string into a list of program names
            names = [name.strip()
                     for name in programs.split(',') if name.strip()]

            programs = []
            for name in names:
                program = Program.query.filter_by(name=name).first()
                if not program:
                    raise NameError("PROGRAM NAME DOES NOT EXIST ", name)

                programs.append(program)

            # Assign the Program instances to the Teacher instance
            teacher.programs = programs

            # LANGUAGES
            langs = ''
            # Get the string of comma seperated languages
            if type(dict_teachers["Vælg de sprog du er helt flydende i"][i]) == str:
                langs = dict_teachers["Vælg de sprog du er helt flydende i"][i]
            # Split the comma-separated string into a list of language names
            names = [name.strip()
                     for name in langs.split(',') if name.strip()]
            langs = []
            for name in names:
                if name == "Persisk":
                    name = "Farsi"
                print(name)
                lang = Language.query.filter_by(name=name).first()
                if not lang:
                    raise NameError("LANGUAGE NAME DOES NOT EXIST ", name)

                langs.append(lang)
            # Assign the Language instances to the Teacher instance
            teacher.languages = langs

            interests = ''
            # Get the string of comma seperated interests
            if type(dict_teachers["Hvad er dine interesser?"][i]) == str:
                interests = dict_teachers["Hvad er dine interesser?"][i]
            # Split the comma-separated string into a list of interests names
            names = [name.strip()
                     for name in interests.split(',') if name.strip()]

            interests = []
            for name in names:
                interest = Interest.query.filter_by(name=name).first()
                if not interest:
                    raise NameError("INTEREST NAME DOES NOT EXIST ", name)

                interests.append(interest)

            # Assign the Program instances to the Teacher instance
            teacher.interests = interests

            # QUALIFICATIONS
            qualifications = ''
            # Get the string of comma seperated interests
            if type(dict_teachers["Kendetegn / Kvalifikationer "][i]) == str:
                qualifications = dict_teachers["Kendetegn / Kvalifikationer "][i]
            # Split the comma-separated string into a list of qualifications names
            names = [name.strip()
                     for name in qualifications.split(',') if name.strip()]

            qualifications = []
            for name in names:
                if name in ["Engelsk korrektur/grammatik", "God til sprogundervisning", "Dansk korrektur/grammatik", "Ikke særlig pædagogisk", "God til SRP-forløb"]:
                    continue
                qualification = Qualification.query.filter_by(
                    name=name).first()
                if not qualification:
                    raise NameError("qualification NAME DOES NOT EXIST ", name)

                qualifications.append(qualification)

            # Assign the Program instances to the Teacher instance
            teacher.qualifications = qualifications
            name = ''
            # Add higher education programme
            if type(dict_teachers["Hvis du går på en videregående uddannelse. Hvilken uddannelse læser du så på?"][i]) == str:
                name = dict_teachers["Hvis du går på en videregående uddannelse. Hvilken uddannelse læser du så på?"][i]
            higher_education = HigherEducationProgramme.query.filter_by(
                name=name).first()
            if higher_education is not None:
                teacher.higher_education_programmes = [higher_education]

            name = ''
            # Add higher education institution
            if type(dict_teachers["Videregående uddannelsesinstitution"][i]) == str:
                name = dict_teachers["Videregående uddannelsesinstitution"][i]
            higher_education = HigherEducationInstitution.query.filter_by(
                name=name).first()

            if higher_education is not None:
                teacher.higher_education_institutions = [higher_education]

            name = ''
            if type(dict_teachers["Gymnasietype "][i]) == str:
                name = dict_teachers["Gymnasietype "][i]
            # Add high school
            high_school = HighSchool.query.filter_by(name=name).first()
            if high_school is not None:
                teacher.high_school = [high_school]

            db.session.add(teacher)
            db.session.commit()
            print(teacher)
            print(first_name, " ", last_name, " successfully added")

    print("All tutors have been added")


@fake.cli.command()
def dborders():
    pass


@fake.cli.command()
def dropall():
    db.drop_all()


@fake.cli.command()
def delete():
    from models.higher_education_programme import teachers_programmes
    from models.higher_education_institution import teachers_institutions
    from models.high_school import teachers_highschool
    from models.interest import teachers_interests
    from models.relationships import tutor_subject
    from models.qualification import teachers_qualifications
    from models.language import teachers_languages
    from models.teacher import teachers_subjects
    from models.program import teachers_programs

    db.session.execute(teachers_interests.delete())
    db.session.execute(teachers_languages.delete())
    db.session.execute(teachers_qualifications.delete())
    db.session.execute(tutor_subject.delete())
    db.session.execute(teachers_highschool.delete())
    db.session.execute(teachers_programmes.delete())
    db.session.execute(teachers_institutions.delete())
    db.session.execute(teachers_programs.delete())
    db.session.execute(teachers_subjects.delete())

    db.session.query(Teacher).delete()
    db.session.query(Student).delete()
    db.session.query(Lesson).delete()
    db.session.query(Transaction).delete()
    db.session.query(WagePayment).delete()
    db.session.query(Balance).delete()
    db.session.query(Customer).delete()
    db.session.query(Admin).delete()
    db.session.query(User).delete()

    db.session.commit()

    Admin.add_new_admin(email="elmar@toptutors.dk", password="admin")
