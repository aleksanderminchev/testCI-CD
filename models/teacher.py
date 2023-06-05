import enum
from numbers import Number
from decouple import config
from flask import abort,current_app,render_template
import requests
from sqlalchemy.orm import validates
import re
from api.app import db
from api.utils.utils import Updateable, get_date
from models.student import GenderEnum, Student
from models.user import User
from models.high_school import HighSchool
from models.higher_education_institution import HigherEducationInstitution
from models.higher_education_programme import HigherEducationProgramme
from models.qualification import Qualification
from models.interest import Interest
from models.program import Program
from models.language import Language
from models.subjects import Subjects
from models.referral import Referral
from api.email import send_email

gmaps_key = config("GOOGLE_MAPS_API_KEY")

teachers_students = db.Table('teacher_students',
                             db.Column('student_id', db.Integer, db.ForeignKey(
                                 'student.id'), primary_key=True, index=True),
                             db.Column('teacher_id', db.Integer,
                                       db.ForeignKey('teacher.id'), primary_key=True,
                                       index=True))

teachers_subjects = db.Table('teacher_subjects',
                             db.Column('subject_id', db.Integer, db.ForeignKey(
                                 'subjects.uid'), primary_key=True, index=True),
                             db.Column('teacher_id', db.Integer,
                                       db.ForeignKey('teacher.id'), primary_key=True,
                                       index=True))


class TeacherStatus(enum.Enum):
    """
    To add this type in migration add:
    from sqlalchemy.dialects import postgresql
    student_status = postgresql.ENUM(
        'active', 'inactive', 'prospective', name='teacherstatus')
    student_status.create(op.get_bind())
    """
    ACTIVE = "active"
    INACTIVE = "inactive"
    PROSPECTIVE = 'prospective'


class Teacher(Updateable, db.Model):  # type:ignore
    """
    The model for Teachers.
    Inheritance from User DB Model. Relation to one user.
    Relation to one, or more Students (Many-to-Many).
    Relation to one, or more Lessons (One-to-Many):One Teacher to many Lessons.
    """

    __tablename__ = "teacher"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.uid'), index=True)
    # TODO add these two rows
    created_on_tw_at = db.Column(
        db.DateTime, nullable=False, default=get_date)
    updated_on_tw_at = db.Column(
        db.DateTime, nullable=False, default=get_date, onupdate=get_date)
    created_at = db.Column(db.DateTime, nullable=True, default=get_date)
    last_updated = db.Column(db.DateTime, nullable=True,
                             default=get_date, onupdate=get_date)
    hire_date = db.Column(db.DateTime, nullable=True, default=get_date)
    wage_per_hour = db.Column(db.Float, nullable=False)
    age = db.Column(db.Integer, nullable=True)
    grade_average = db.Column(db.Float, nullable=True, server_default='0')
    bio = db.Column(db.Text, nullable=True)
    photo = db.Column(db.String, nullable=True)
    open_for_new_students = db.Column(
        db.Boolean, default=True, server_default='f', nullable=False,
        index=True)
    # payroll id is cpr number
    payroll_id = db.Column(db.String, nullable=True)
    bank_number = db.Column(db.String, nullable=True)
    reg_number = db.Column(db.String, nullable=True)
    address = db.Column(db.String, nullable=True)
    zip_code = db.Column(db.String, nullable=True)
    country = db.Column(db.String, nullable=True)
    city = db.Column(db.String, nullable=True)
    how_they_found = db.Column(db.String, nullable=True)
    finished_highschool = db.Column(
        db.Boolean, default=True, server_default='t', nullable=False)
    birthday = db.Column(db.DateTime, nullable=True)
    # lat d.
    lat = db.Column(db.String, nullable=True)
    # lng d.
    lng = db.Column(db.String, nullable=True)
    # lat_alternative d.
    lat_alternative = db.Column(db.String, nullable=True)
    # lng_alternative d.
    lng_alternative = db.Column(db.String, nullable=True)
    internal_note = db.Column(db.Text, nullable=True)
    application_reason = db.Column(db.Text, nullable=True)
    # status d. as field status
    # gym_type d.
    gender = db.Column(
        db.Enum(
            GenderEnum,
            values_callable=lambda obj: [e.value for e in obj]
        ),
        nullable=True,
        default=GenderEnum.MALE.value,
        server_default=GenderEnum.MALE.value,
        index=True
    )
    status = db.Column(
        db.Enum(
            TeacherStatus,
            values_callable=lambda obj: [e.value for e in obj]
        ),
        nullable=False,
        default=TeacherStatus.PROSPECTIVE.value,
        server_default=TeacherStatus.PROSPECTIVE.value,
        index=True
    )
    age_interval = db.Column(db.String, nullable=True)
    # inactive_reason
    inactive_reason = db.Column(db.String, nullable=True)
    # has_second
    has_second = db.Column(db.String, nullable=True)
    # still_gym as finished_highschool boolean field
    # tutor_gym I am guessing as field teacher.highschool
    # hours
    hours = db.Column(db.Integer, nullable=True)
    # hour_interval
    hour_interval = db.Column(db.String, nullable=True)
    # tutor_qualification as teacher.qualifications relantionship
    # tutor_uni as teacher.higher_education_institution relantionship
    # tutor_address d. as address
    # tutor_amount_of_students  as field teacher.students relantionship
    # teachworks profile URL
    teachworks = db.Column(db.String, nullable=True)

    # One Teacher to Many Courses
    courses = db.relationship("Course", backref="teacher")

    # One Teacher to Many Lessons
    lessons_teacher = db.relationship('Lesson',
                                      backref='lessons_teacher')

    # Many Teachers to Many Students
    students = db.relationship("Student", secondary=teachers_students, primaryjoin=(
        teachers_students.c.teacher_id == id), backref='teachers')
    marketing_consent = db.Column(db.Boolean, default=False)

    # Many Teachers to Many Subjects
    subjects = db.relationship("Subjects", secondary=teachers_subjects, primaryjoin=(
        teachers_subjects.c.teacher_id == id), backref='teachers')

    referred = db.relationship("Referral", primaryjoin=(
        id == Referral.referred_id), backref='referred', uselist=False)
    referrals = db.relationship("Referral", primaryjoin=(
        id == Referral.referrer_id), backref='referrals')

    def to_calendar(self):
        return {
            "students":[i.id for i in (self.students or [])],
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "email": self.user.email,
            'id': self.id,
            'status': self.status.value,
        }



    def to_dict(self):

        if hasattr(self.referred, 'referred_id'):
            referred = self.referred.referrer_id
        else:
            referred = ''
        return {
            "first_name": getattr(self, 'user.first_name',""),
            "last_name": getattr(self, 'user.last_name',""),
            "phone":  getattr(self, 'user.phone',""),
            "hire_date": self.hire_date,
            "wage_per_hour": self.wage_per_hour,
            "bio": self.bio,
            "birthday": self.birthday,
            "address": self.address,
            "city": self.city,
            "zip_code": self.zip_code,
            "country": self.country,
            "bank_number": self.bank_number,
            "reg_number": self.reg_number,
            "grade_average": self.grade_average,
            'how_they_found': self.how_they_found,
            "photo": self.photo,
            "gender": self.gender.value,
            "open_for_new_students": self.open_for_new_students,
            "payroll_id": self.payroll_id,
            'students': [i.id for i in (self.students or [])],
            "high_school": [i.to_dict() for i in (self.high_school or [])],
            "finished_highschool": self.finished_highschool,
            "languages": [i.to_dict() for i in (self.languages or [])],
            "programs": [i.to_dict() for i in (self.programs or [])],
            "qualifications": [i.to_dict() for i in (self.qualifications or [])],
            "interests": [i.to_dict() for i in (self.interests or [])],
            "subjects": [i.to_dict() for i in (self.subjects or [])],
            "higher_education_institutions": [i.to_dict() for i in (self.higher_education_institutions or [])],
            "higher_education_programmes": [i.to_dict() for i in (self.higher_education_programmes or [])],
            "last_login":getattr(self, 'user.last_login',""),
            "is_verified": getattr(self, 'user.is_verified',""),
            "email": getattr(self, 'user.email',""),
            'id': self.id,
            'age': self.age,
            'status': self.status.value,
            'created_at': self.created_at,
            "last_updated": self.last_updated,
            "created_on_tw_at": self.created_on_tw_at,
            "updated_on_tw_at": self.updated_on_tw_at,
            "lat": self.lat,
            "lng": self.lng,
            "lat_alternative": self.lat_alternative,
            "lng_alternative": self.lng_alternative
        }

    def age_and_grade_interval_tutor_map(self, age, grade):
        age_interval = 'under 18'
        if age >= 18 and age <= 20:
            age_interval = '18 til 20'
        elif age >= 21 and age <= 23:
            age_interval = '21 til 23'
        elif age >= 24 and age <= 26:
            age_interval = '24 til 26'
        elif age >= 27:
            age_interval = '27+'
        grade_interval = 'Under 7'
        if grade >= 7 and grade <= 8:
            grade_interval = '7 til 8'
        elif grade >= 8 and grade <= 9:
            grade_interval = '8 til 9'
        elif grade >= 9 and grade <= 10:
            grade_interval = '9 til 10'
        elif grade >= 10 and grade <= 11:
            grade_interval = '10 til 11'
        elif grade >= 11 and grade <= 12:
            grade_interval = '11 til 12'
        elif grade > 12:
            grade_interval = 'Over 12'
        return {"age_interval": age_interval, "grade_interval": grade_interval}

    def to_tutormap(self):
        hours = 0
        for i in self.lessons_teacher:
            if i.status.value == 'attended':
                hours += i.duration_in_minutes/60
        today = get_date()
        birthday = self.birthday or get_date()
        age = today.year - birthday.year - \
            ((today.month, today.day) < (birthday.month, birthday.day))
        age_grades = self.age_and_grade_interval_tutor_map(
            age, self.grade_average)
        return {
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "phone": self.user.phone,
            "hire_date": self.hire_date,
            "wage_per_hour": self.wage_per_hour,
            "bio": self.bio,
            "birthday": self.birthday,
            "address": self.address,
            "city": self.city,
            "zip_code": self.zip_code,
            "country": self.country,
            "bank_number": self.bank_number,
            "reg_number": self.reg_number,
            "grade_average": age_grades['grade_interval'],
            'how_they_found': self.how_they_found,
            "photo": self.photo,
            "gender": self.gender.value,
            "open_for_new_students": self.open_for_new_students,
            "payroll_id": self.payroll_id,
            'students': [i.id for i in (self.students or [])],
            "high_school": [i.name for i in (self.high_school or [])],
            "finished_highschool": self.finished_highschool,
            "languages": [i.name for i in (self.languages or [])],
            "programs": [i.name for i in (self.programs or [])],
            "qualifications": [i.name for i in (self.qualifications or [])],
            "interests": [i.name for i in (self.interests or [])],
            "subjects": [i.name for i in (self.subjects or [])],
            "higher_education_institutions": [i.name for i in (self.higher_education_institutions or [])],
            "higher_education_programmes": [i.name for i in (self.higher_education_programmes or [])],
            "last_login": self.user.last_login,
            "is_verified": self.user.is_verified,
            "email": self.user.email,
            'id': self.id,
            'age': age,
            'age_interval': age_grades['age_interval'],
            'status': self.status.value,
            'hours': round(hours, 2),
            'created_at': self.created_at,
            "last_updated": self.last_updated,
            "created_on_tw_at": self.created_on_tw_at,
            "updated_on_tw_at": self.updated_on_tw_at,
            "lat": self.lat,
            "lng": self.lng,
            "lat_alternative": self.lat_alternative,
            "lng_alternative": self.lng_alternative
        }

    @validates("wage_per_hour")
    def validate_wage_per_hour(self, key, wage_per_hour):
        if not isinstance(wage_per_hour, Number):
            raise ValueError("invalid wage")
        if wage_per_hour < 0:
            raise ValueError("invalid wage")
        return wage_per_hour

    @validates("payroll_id")
    def validate_payroll_id(self, key, payroll_id):
        if not isinstance(payroll_id, str):
            raise ValueError("invalid cpr")
        if len(payroll_id) != 11:
            raise ValueError("invalid cpr")
        if not re.match(r"\d{6}-\d{4}", payroll_id):
            raise ValueError("invalid cpr")
        return payroll_id

    @staticmethod
    def get_tutors_by_filters(filters: dict):
        """ Returns all tutors after applying the filters. 
        Gets returned in the to_tutormap format.
        """

        query = db.session.query(Teacher)

        # Apply filters to the query
        for column, value in filters.items():
            if column == "subjects":
                for subject in value:
                    # Apply filter for each subject
                    query = query.filter(
                        Teacher.subjects.any(Subjects.name == subject))
            else:
                query = query.filter(getattr(Teacher, column) == value)

        # Execute the query and retrieve the tutors
        result = query.all()

        return [tutor.to_tutormap() for tutor in result]

    @staticmethod
    def all_tutors(active=False):
        """ Gets all tutors that are not prospective and formats the result.

        Set active = True if you don't want inactive tutors. 
        """
        if active:
            result = Teacher.query.filter(
                Teacher.status == TeacherStatus.ACTIVE
            ).all()
        else:
            result = Teacher.query.filter(
                Teacher.status != TeacherStatus.PROSPECTIVE
            ).all()

        return [tutor.to_tutormap() for tutor in result]

    @staticmethod
    def add_new_tutor(data):  # DEPRECATED? Remove this and all uses of this? TODO
        """Adds a new lesson to the DB.
        Data argument is a dictionary containing lesson data from TW.
        """
        teacher = Teacher(**data)
        db.session.add(teacher)
        db.session.commit()

    def validate_tutor_address(self):
        lat = 0
        lng = 0
        if self.lat == 0 and self.lng == 0:
            if self.address == "":
                return
            address = f"{self.address} {self.city} {self.zip_code}"
            response = requests.get(
                "https://maps.googleapis.com/maps/api/geocode/json?",
                params={"key": gmaps_key, "address": address},
            ).json()
            print(response)
            response.keys()
            if response["status"] == "OK":
                geometry = response["results"][0]["geometry"]
                self.lat = geometry["location"]["lat"]
                self.lng = geometry["location"]["lng"]
            db.session.commit()
        return

    @staticmethod
    def add_new_teacher(**kwargs):
        """ Adds a new teacher to the DB. TODO """
        user = User(
            email=kwargs['email'],
            password='',
            first_name=kwargs['first_name'],
            last_name=kwargs['last_name'], phone=kwargs['phone'])
        db.session.add(user)
        db.session.commit()

        # birthday=datetime.datetime.strptime(kwargs['birthday'])
        teacher = Teacher(
            user_id=user.uid,
            grade_average=kwargs.get('grade_average'),
            wage_per_hour=kwargs.get('wage_per_hour'),
            bio=kwargs.get('bio'),
            photo=kwargs.get('photo'),
            age=kwargs.get('age'),
            gender=kwargs.get('gender'),
            birthday=kwargs.get('birthday'),
            bank_number=kwargs.get('bank_number'),
            reg_number=kwargs.get('reg_number'),
            country=kwargs.get('country'),
            address=kwargs.get('address'),
            city=kwargs.get('city'),
            zip_code=kwargs.get('zip_code'),
            status=kwargs.get('status'),
            payroll_id=kwargs.get('payroll_id'),
            how_they_found=kwargs.get('how_they_found'),
            open_for_new_students=kwargs.get('open_for_new_students'),
            finished_highschool=kwargs.get('finished_highschool'),
        )
        db.session.add(teacher)
        db.session.commit()
        # subjects and math programms(optional) both multiple
        # optional for others
        teacher.validate_tutor_address()
        if 'highschool' in kwargs.keys():
            HighSchool.add_high_school_to_teacher(
                kwargs['highschool'], teacher)

        if 'higher_education_institution' in kwargs.keys():
            HigherEducationInstitution.add_higher_edu_institution_to_teacher(
                kwargs['higher_education_institution'], teacher)

        if 'higher_education_programme' in kwargs.keys():
            HigherEducationProgramme.add_higher_edu_programme_to_teacher(
                kwargs['higher_education_programme'], teacher)

        if 'qualification' in kwargs.keys():
            Qualification.add_qualification_to_teacher(
                teacher, kwargs['qualification'])

        if 'interest' in kwargs.keys():
            Interest.add_interest_to_teacher(
                teacher, kwargs['interest'])

        if 'language' in kwargs.keys():
            Language.add_language_to_teacher(
                teacher, kwargs['language'])

        if 'subjects_create' in kwargs.keys():
            for i in kwargs['subjects_create']:
                Subjects.add_subject_to_teacher(i, teacher)

        if 'programs_create' in kwargs.keys():
            for i in kwargs['programs_create']:
                Program.add_program_to_teacher(teacher, i)
        if 'referred_by' in kwargs.keys() and 'referral_amount' in kwargs.keys():
            Referral.add_new_referral(referrer_id=kwargs['referred_by'],
                                      referred_id=teacher.id,
                                      referral_amount=kwargs['referral_amount'])
        if user is not None:
            reset_token = user.generate_reset_token()
            reset_url = current_app.config['CONFIRMATION_URL'] + \
                '?token=' + reset_token
            template = render_template(
                "email/verify-email.html",
                token=reset_token,
                confirm_url=reset_url
            )
            send_email([teacher.user.email], 'Confirm your account', template)
        return teacher

    @ staticmethod
    def add_student_to_teacher(student_id, teacher_email):
        teacher_user = User.find_by_email(teacher_email)
        print(student_id)
        print(teacher_email)
        students = []
        for i in student_id:
            student = Student.get_student_by_id(i)
            students.append(student)
            print(students)
            teacher_user.teacher.students = students
            db.session.add(teacher_user)
            db.session.commit()
        return teacher_user.teacher.students

    @ staticmethod
    def remove_student_from_teacher(student_id, teacher_email):
        teacher_user = User.find_by_email(teacher_email)
        student = Student.get_student_by_id(student_id)
        students = teacher_user.teacher.students
        if student not in students:
            abort(500)
        students.remove(student)
        db.session.add(teacher_user)
        db.session.commit()
        return students

    @ staticmethod
    def delete_teacher(id: str):
        """Deletes a teacher from the DB"""
        teacher = Teacher.query.get(id) or abort(404)
        return_dictionary = teacher.to_dict()
        db.session.delete(teacher)
        db.session.commit()
        return return_dictionary

    @ staticmethod
    def filter_teachers(**kwargs):
        from models.teacher_view import TeacherView
        # if kwargs['first_name'] or kwargs['last_name']:
        # arguments_for_user={key:value for key, value in kwargs.items() if key in ('first_name', 'last_name', 'email','phone')}
        arguments_for_user = {}
        arguments_for_teacher = {}
        arguments_for_relantionships = {}
        for key, value in kwargs.items():
            if key in ('first_name', 'last_name', 'email', 'phone'):
                arguments_for_user[key] = value
            elif key in ('higher_education_institution', 'higher_education_programme', 'qualification', 'subject', 'language', 'lesson', 'interest', 'program'):
                arguments_for_relantionships[key+"_id"] = value
            else:
                arguments_for_teacher[key] = value
                # arguments_for_teacher[key]= value

        all_teachers_filtered = {}
        if arguments_for_user or arguments_for_teacher:
            all_teachers_filtered = db.session.query(Teacher).filter_by(**arguments_for_teacher).join(
                User).filter(Teacher.user_id == User.uid).filter_by(**arguments_for_user).all()
        filteringby_relantion = {}
        if arguments_for_relantionships:
            # use this to filter the many relationships
            filteringby_relantion = TeacherView.query.filter_by(
                **arguments_for_relantionships).all()
            # convert the teacherview objects to a teacher set
            # since the many joins create duplicates for the amount of teachers
            filteringby_relantion = TeacherView.convert(filteringby_relantion)
        all_teachers_filtered = set(all_teachers_filtered)
        all_teachers_filtered = all_teachers_filtered.union(
            filteringby_relantion)
        return_array = [i.to_dict() for i in all_teachers_filtered]
        return return_array

    @ staticmethod
    def get_teacher_by_id(teacher_id: int):
        """Gets a teacher by the id from the DB"""
        return Teacher.query.get(teacher_id)

    @ staticmethod
    def get_teacher_by_email(email: str, abort: bool = True):
        """Gets a teacher by the email from the DB
        As a default it aborts if teacher is not found. To disable this pass abort=False"""
        if abort:
            user = User.query.filter_by(email=email).first() or abort(404)
        else:
            user = User.query.filter_by(email=email).first() or abort(404)
        return user.teacher

    @ staticmethod
    def update_teacher(id: int, **kwargs):
        """Updates a teacher by the id from the DB"""
        arguments_for_user = {}
        arguments_for_teacher = {}
        arguments_for_array = {
            'high_school_update': [],
            'higher_education_institutions_update': [],
            'higher_education_programmes_update': [],
            'qualifications_update': [],
            'subjects_update': [],
            'languages_update': [],
            'interests_update': [],
            'programs_update': []
        }

        for key, value in kwargs.items():
            if key in ('first_name', 'last_name', 'phone', 'email'):
                arguments_for_user[key] = value
            elif key in (
                'high_school_update',
                'higher_education_institutions_update',
                'higher_education_programmes_update',
                'qualifications_update',
                'subjects_update',
                'languages_update',
                'programs_update',
                'interests_update'
            ):
                arguments_for_array[key] = value
            else:
                arguments_for_teacher[key] = value

        teacher = Teacher.query.get(id) or abort(404)
        User.update(teacher.user, arguments_for_user)
        Teacher.update(teacher, arguments_for_teacher)
        if 'wage_per_hour' in kwargs.keys():
            today = get_date()
            wage_per_hour = kwargs.get('wage_per_hour')
            for i in teacher.lessons_teacher:
                status_value = i.status.value
                duration = i.duration_in_minutes/60
                if (i.from_time >= today
                    and status_value != 'good cancellation'
                        and status_value != 'bad cancellation teacher'):

                    i.wage = duration * wage_per_hour
        if 'higher_education_institutions_update' in kwargs.keys():
            teacher.higher_education_institutions = []
            for i in arguments_for_array['higher_education_institutions_update']:
                HigherEducationInstitution.add_higher_edu_institution_to_teacher(
                    i, teacher)

        if 'higher_education_programmes_update' in kwargs.keys():
            teacher.higher_education_programmes = []
            for i in arguments_for_array['higher_education_programmes_update']:
                HigherEducationProgramme.add_higher_edu_programme_to_teacher(
                    i, teacher)

        if 'programs_update' in kwargs.keys():
            teacher.programs = []
            for i in arguments_for_array['programs_update']:
                Program.add_program_to_teacher(teacher, i)

        if 'qualifications_update' in kwargs.keys():
            teacher.qualifications = []
            for i in arguments_for_array['qualifications_update']:
                Qualification.add_qualification_to_teacher(
                    teacher, i)

        if 'interests_update' in kwargs.keys():
            teacher.interests = []
            for i in arguments_for_array['interests_update']:
                Interest.add_interest_to_teacher(teacher, i)

        if 'subjects_update' in kwargs.keys():
            print(arguments_for_array['subjects_update'], "subjects is rnu")
            teacher.subjects = []
            for i in arguments_for_array['subjects_update']:
                Subjects.add_subject_to_teacher(i, teacher)

        if 'languages_update' in kwargs.keys():
            teacher.languages = []
            for i in arguments_for_array['languages_update']:
                Language.add_language_to_teacher(teacher, i)

        if 'high_school_update' in kwargs.keys():
            teacher.high_school = []
            for i in arguments_for_array['high_school_update']:
                HighSchool.add_high_school_to_teacher(i, teacher)

        db.session.commit()
        return teacher.to_dict()
