import os
import requests
import pickle
import ast
import json

from decouple import config
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models.tutor import Tutor
from models.subjects import Subjects
from api.services.tw.lessons import update_and_calculate_lesson_hours
from api.services.tw.tutor_students import get_tutor_students
from api.services.tw.tw_api_utils import get_subjects, get_tutor_list


GYM_TYPE_FIELD_ID = 10214
CPR_FIELD_ID = 10221
TUTOR_REFERAL_ID = 10701
GENDER_ID = 11577
ACCESS_CAR = 11722
GRADE_AVERAGE = 11723
TUTOR_COURSE = 11724
TUTOR_WANTED_COURSE = 12604
TUTOR_PROGRAMS = 11719
TUTOR_FLUENT_DANISH = 11590
TUTOR_FLUENT_IN_OTHER_LANGUAGES = 11717
TUTOR_OPEN_FOR_COURSES = 11064
TUTOR_EDUCATIONAL_INSTITUTION = 11718
TUTOR_SECOND_ADRESS = 11721
TUTOR_INACTIVE_REASON = 11591
TUTOR_STILL_IN_GYM = 12027
TUTOR_GYM = 12026
TUTOR_QUALIFICATION = 12179
TUTOR_UNI = 12199
TUTOR_INTERESTS = 14019

uni_uddannelser = []
language_list = []
tutor_qualification_list = []
tutor_interests_list = []
gyms = []
gmaps_key = config("GOOGLE_MAPS_API_KEY")

if config("CONFIG_NAME") == "production":
    send_mail = False  # Ændre den her til True i production
else:
    send_mail = True  # Ændre den her til True i production


if config("CONFIG_NAME") == "production":
    engine = create_engine(config("SQLALCHEMY_DATABASE_URI"))
else:
    engine = create_engine(config("SQLALCHEMY_DATABASE_URI_TEST"))


def blacklist(tutor):
    """
    dorde
    """
    blacklisted = ["Elmar", "Johannsson", "TEST",
                   "TEST", "Hasan", "Tutor", "Nadia", "Test"]

    if tutor["first_name"] in blacklisted and tutor["last_name"] in blacklisted:
        return True
    return False


def subjects_missing(subjects):
    """Returns a list of missing subjects. I.e if a tutor has Matematik A, it will return [Matematik B, Matematik C]"""

    filters = ["Folkeskole", "C", "B", "A"]
    subjects_to_add = 0
    remaining_subjects = []

    for subject in subjects:
        if subject[-1] in filters:
            subjects_to_add = filters.index(subject[-1])
            for i in range(subjects_to_add):
                remaining_subjects.append(subject[:-1] + filters[i])
    return remaining_subjects


def update_subjects():
    """Updates a pickle with a list of all subjects on TW."""
    subjects_data = get_subjects()
    subjects_list = []
    for subject in subjects_data:
        if isinstance(subject, dict):
            if subject["name"] != "":
                data = {
                    "subject": subject["name"]
                }
                subjects_list.append(data)

                subjects_list = sorted(
                    subjects_list, key=lambda i: i['subject'])
                # Add all the new data to our pickle file,
                # and overwrite previous data
                pickle.dump(subjects_list, open("pickles/subject.p", "wb"))


def populate_subjects_in_db():

    subjects_data = get_subjects()
    subjects_list = []

    if len(subjects_data) == 0:
        return
    with Session(engine) as session:
        Subjects.delete(session)  # Clear tablet så der ikke kommer duplicates.
        for subject in subjects_data:
            subject_to_add = Subjects.add(subject["name"])
            session.add(subject_to_add)
            print(subject_to_add.subject)

        session.commit()


def update_qualifications(tutor_data):

    tutor_qualification = tutor_data["tutor_qualification"]
    for x in tutor_qualification:
        if len(x) <= 1:
            continue

        if x in tutor_qualification_list:
            continue

        else:
            tutor_qualification_list.append(x)
    pickle.dump(tutor_qualification_list, open(
        "pickles/tutor_qualifications.p", "wb"))


def update_interests(tutor_data):
    tutor_interest = tutor_data["tutor_interests"]
    for x in tutor_interest:
        if len(x) <= 1:
            continue

        if x in tutor_interests_list:
            continue

        else:
            tutor_interests_list.append(x)
    pickle.dump(tutor_interests_list, open("pickles/tutor_interest.p", "wb"))


def update_languages(tutor_data):
    language = tutor_data["fluent_other"]
    for x in language:
        if len(x) <= 1:
            continue

        if x in language_list:
            continue

        else:
            language_list.append(x)
    seen = {}
    new_list = [seen.setdefault(x, x) for x in language_list if x not in seen]
    pickle.dump(new_list, open("pickles/languages.p", "wb"))


def validate_tutor_address(tutor):
    """Validate the tutors address"""
    lat = 0
    lng = 0
    if isinstance(tutor, dict):
        if tutor["address"] == "":
            print(f"Skipped {tutor['first_name']} {tutor['last_name']}")
        address = f"{tutor['address']} {tutor['city']} {tutor['zip']}"
        response = requests.get(
            "https://maps.googleapis.com/maps/api/geocode/json?",
            params={"key": gmaps_key, "address": address},
        ).json()
        response.keys()
        if response["status"] == "OK":
            geometry = response["results"][0]["geometry"]
            lat = geometry["location"]["lat"]
            lng = geometry["location"]["lng"]
        else:
            print(
                f"Failed to add {tutor['first_name']} {tutor['last_name']} to the map with error: {response}")
            # if send_mail:
            #     send_error_email_to_admins(tutor, response)
    return lat, lng


def get_tutor_subjects(tutor):
    """
    Gets the subjects of one tutor and formats it.
    """

    if tutor["subjects"] != "":
        filter_subjects = str(tutor["subjects"]).split(',')
        filter_subjects = [s.strip() for s in filter_subjects]
    return filter_subjects


def get_tutor_custom_fields(tutor):
    """
    Gets the custom fields for every tutor
    """
    gym_type = None
    referal = None
    gender = None
    car = None
    course = None
    programs = None
    fluent_danish = None
    fluent_other = None
    more_courses = None
    educational_institution = None
    lat_alternative = 0
    lng_alternative = 0
    has_second = False
    age = None
    inactive_reason = None
    still_gym = None
    tutor_gym = None
    hour_interval = None
    tutor_qualification = None
    tutor_interests = None
    tutor_uni = None
    grade = 0
    age_interval = 0
    wanted_course = []
    bio = tutor["bio"]
    photo = tutor["photo"]
    updated_at = tutor["updated_at"]

    for element in tutor["custom_fields"]:
        if element["field_id"] == GYM_TYPE_FIELD_ID:
            if element["value"] == "":
                gym_type = "Not set by tutor"
            else:
                gym_type = element["value"]

        if element["field_id"] == CPR_FIELD_ID:
            if element["value"] == "" or element["value"] is None:
                pass
            else:
                # calcuate the age between two dates
                today = dt.now()
                cpr = element["value"]

                cpr = cpr[:6]
                date = cpr[:2]
                if date[0] == "0":
                    date = date[1:2]

                month = cpr[2:4]
                if month[0] == "0":
                    month = month[1:2]

                try:
                    year = cpr[4:6]
                    if int(year) in range(0, int(str(today.year)[:2])+1):
                        year = "20" + year
                    else:
                        year = "19" + year

                    birth_date = dt(int(year), int(month), int(date))

                    age = relativedelta(today, birth_date).years
                except Exception:
                    age = 0

                if age < 18:
                    age_interval = "under 18"
                elif age >= 18 and age <= 20:
                    age_interval = "18 til 20"
                elif age >= 21 and age <= 23:
                    age_interval = "21 til 23"
                elif age >= 24 and age <= 26:
                    age_interval = "24 til 26"
                elif age >= 27:
                    age_interval = "27+"
                else:
                    print("we made a mistake")

        if element["field_id"] == TUTOR_REFERAL_ID:
            if element["value"] is None:
                referal = "N/A"
            else:
                referal = element["value"]

        if element["field_id"] == GENDER_ID:
            if element["value"] == "" or element["value"] is None:
                gender = "Not set by tutor"
            else:
                gender = element["value"]

        if element["field_id"] == ACCESS_CAR:
            if element["value"] is None or element["value"] == '0':
                car = "No"
            else:
                car = "Yes"

        if element["field_id"] == GRADE_AVERAGE:
            if element["value"] is None or element["value"] == '0':
                grade = "Not set by tutor"
            else:
                grade = element["value"]

        if element["field_id"] == TUTOR_COURSE:
            if element["value"] is None or element["value"] == '0':
                course = "Not set by tutor"
            else:
                course = element["value"]

        if element["field_id"] == TUTOR_WANTED_COURSE:
            if element["value"] is not None:
                filter_course = str(element["value"]).split(',')
                for x in filter_course:
                    wanted_course.append(x)

        if element["field_id"] == TUTOR_PROGRAMS:
            if element["value"] is None or element["value"] == "":
                programs = "Not set by tutor"
            else:
                formatted_programs = ""
                programs = str(element["value"]).split(", ")
                for x in programs:
                    formatted_programs += x + ", "

        if element["field_id"] == TUTOR_FLUENT_DANISH:
            if element["value"] is None or element["value"] == '0':
                fluent_danish = "Not set by tutor"
            else:
                fluent_danish = "Yes"

        if element["field_id"] == TUTOR_OPEN_FOR_COURSES:
            if element["value"] is None or element["value"] == "":
                more_courses = "Yes"
            elif element["value"] == "Jeg vil ikke have flere forløb i øjeblikket":
                more_courses = "No"
            else:
                more_courses = "Yes"

        if element["field_id"] == TUTOR_EDUCATIONAL_INSTITUTION:
            if element["value"] is None or element["value"] == "":
                educational_institution = "Not set by tutor"
            else:
                educational_institution = element["value"]

        if element["field_id"] == TUTOR_FLUENT_IN_OTHER_LANGUAGES:
            if element["value"] is None or element["value"] == '0':
                fluent_other = "Not set by tutor"
            else:
                formatted_fluent = ""
                fluent_other = str(element["value"]).split(", ")
                for x in fluent_other:
                    formatted_fluent += x + ", "

        # If there is no address from the tutor, we skip it
        if element["field_id"] == TUTOR_SECOND_ADRESS:
            # if second adress is not filled
            if element["value"] is None or element["value"] == "":
                print()
            else:  # second adress is not empty, so let's get the cordinates from google.
                # We string a long address that is used to geocode the lat & lng
                # the alternative address
                alternative_address = element["value"]
                alternative_response = requests.get(
                    "https://maps.googleapis.com/maps/api/geocode/json?",
                    params={"key": gmaps_key, "address": str(
                        alternative_address)},
                ).json()

                # If we got a good response, then we add the lat & lng
                if alternative_response["status"] == "OK":
                    alternative_geometry = alternative_response["results"][0]["geometry"]
                    lat_alternative = alternative_geometry["location"]["lat"]
                    lng_alternative = alternative_geometry["location"]["lng"]
                    has_second = True
                    # print("SUCCESS at getting alternative address.")

        if element["field_id"] == TUTOR_INACTIVE_REASON:
            if element["value"] is None or element["value"] == "":
                inactive_reason = "Blank"
            else:
                inactive_reason = element["value"].replace(
                    '\n', '').replace('\r', '')

        if element["field_id"] == TUTOR_STILL_IN_GYM:
            if element["value"] is None or element["value"] == "":
                still_gym = "Not set by tutor"
            else:
                still_gym = element["value"]

        if element["field_id"] == TUTOR_GYM:
            if element["value"] is None or element["value"] == "":
                tutor_gym = "Not set by tutor"
            else:
                tutor_gym = element["value"]
                if element["value"] in gyms:
                    pass
                else:
                    gyms.append(element["value"])

        if element["field_id"] == TUTOR_QUALIFICATION:
            if element["value"] is None or element["value"] == '0':
                tutor_qualification = "Not set by tutor"
            else:
                tutor_qualification = str(element["value"]).split(", ")

        if element["field_id"] == TUTOR_INTERESTS:
            if element["value"] is None or element["value"] == '0':
                tutor_interests = "Not set by tutor"
            else:
                tutor_interests = str(element["value"]).split(", ")

        if element["field_id"] == TUTOR_UNI:
            if element["value"] is None or element["value"] == "" or element["value"] == "Går ikke på en videregående uddannelse":
                tutor_uni = "Går ikke på en videregående uddannelse"
            else:
                tutor_uni = element["value"]
                if element["value"] in uni_uddannelser:
                    pass
                else:
                    uni_uddannelser.append(tutor_uni)
    return gym_type, referal, gender, car, course, programs, fluent_danish, fluent_other, more_courses, educational_institution, lat_alternative, lng_alternative, has_second, age, inactive_reason, still_gym, tutor_gym, hour_interval, tutor_qualification, tutor_uni, grade, age_interval, wanted_course, bio, photo, updated_at, tutor_interests


def get_tutor_amount_of_students(tutor):
    """
    dorde
    """
    tutor_amount_of_students = 0
    if os.path.exists("pickles/sorted_amount_of_students.p"):
        if os.path.getsize("pickles/sorted_amount_of_students.p") > 0:
            students = pickle.load(
                open("pickles/sorted_amount_of_students.p", "rb"))

            for student in students:
                if student["id"] == tutor["id"]:
                    tutor_amount_of_students = student["students"]
            return tutor_amount_of_students


def calculate_tutor_hours(tutor):
    """
    dorde
    """
    hour = 0
    hour_interval = ""
    if os.path.exists("pickles/lessons_filtered.p"):
        if os.path.getsize("pickles/lessons_filtered.p") > 0:
            tutors_hour_list = pickle.load(
                open("pickles/lessons_filtered.p", "rb"))

        for h in tutors_hour_list:  # tjek om id'erne matcher
            if h["id"] == tutor["id"]:
                hour = round(h["hours"], 2)
                if hour >= 0 and hour <= 2:
                    hour_interval = "0 til 2"
                    # print("0 til 2")
                elif hour >= 2 and hour <= 10:
                    hour_interval = "2 til 10"
                    # print("2 til 10")
                elif hour >= 10 and hour <= 50:
                    hour_interval = "10 til 50"
                    # print("10 til 50")
                elif hour >= 50 and hour <= 100:
                    hour_interval = "50 til 100"
                    # print("100+")
                elif hour >= 100:
                    hour_interval = "100+"
                else:
                    print(f"FEJL!! {hour}")
        return hour, hour_interval


def update_tutor_pickle():
    """
    dorde
    """
    tutor_list = []
    update_and_calculate_lesson_hours()
    update_subjects()
    for tutor in get_tutor_list():
        if tutor["status"] == "Prospective":
            continue
        lat, lng = validate_tutor_address(tutor)
        subjects = get_tutor_subjects(tutor)
        subjects.extend(subjects_missing(subjects))
        tutor_amount_of_students = get_tutor_amount_of_students(tutor)
        formatted_subjects = subjects
        hours, hour_interval = calculate_tutor_hours(tutor)
        gym_type, referal, gender, car, course, programs, fluent_danish, fluent_other, more_courses, educational_institution, lat_alternative, lng_alternative, has_second, age, inactive_reason, still_gym, tutor_gym, hour_interval, tutor_qualification, tutor_uni, grade, age_interval, wanted_course, bio, photo, updated_at, tutor_interests = get_tutor_custom_fields(
            tutor)
        tutor_data = {
            "id": tutor["id"],
            "first_name": tutor["first_name"],
            "last_name": tutor["last_name"],
            "email": tutor["email"],
            "mobile_phone": tutor["mobile_phone"],
            "lat": lat,
            "lng": lng,
            "lat_alternative": lat_alternative,
            "lng_alternative": lng_alternative,
            "status": tutor["status"],
            "gym_type": gym_type,
            "gender": gender,
            "car": car,
            "grade": grade,
            "course": course,
            "programs": programs,
            "fluent_danish": fluent_danish,
            "fluent_other": fluent_other,
            "more_courses": more_courses,
            "educational_institution": educational_institution,
            "age": age,
            "age_interval": age_interval,
            "subjects": subjects,
            "inactive_reason": inactive_reason,
            "has_second": has_second,
            "still_gym": still_gym,
            "tutor_gym": tutor_gym,
            "hours": round(hours, 2),
            "hour_interval": hour_interval,
            "tutor_qualification": tutor_qualification,
            "tutor_uni": tutor_uni,
            "tutor_address": tutor["address"],
            "tutor_amount_of_students": tutor_amount_of_students,
            "formatted_subjects": formatted_subjects,
            "tutor_interests": tutor_interests,
            "teachworks": f"https://toptutors.teachworks.com/employees/{tutor['id']}",
            "wanted_course": wanted_course,
            "bio": bio,
            "photo": photo,
            "updated_at": updated_at
        }
        tutor_list.append(tutor_data)

        update_languages(tutor_data)
        update_qualifications(tutor_data)
        update_interests(tutor_data)

        Add_tutor_to_db(tutor_data)

    tutor_list = sorted(tutor_list, key=lambda i: i['hours'])
    tutor_list = sorted(
        tutor_list, key=lambda i: i['tutor_amount_of_students'])

    # List of all selected university educations
    pickle.dump(uni_uddannelser, open("pickles/uni.p", "wb"))
    pickle.dump(gyms, open("pickles/gyms.p", "wb"))
    # Add all the new data to our pickle file,
    # and overwrite previous data
    pickle.dump(tutor_list, open("pickles/tutor.p", "wb"))

    print(len(tutor_list))


def Add_tutor_to_db(tutor_data):
    with Session(engine) as session:
        tutor = Tutor.add_new(tutor_data, session)
        if Tutor.in_db(tutor, session) is False:
            print(tutor.subjects_relationship)
            session.add(tutor)
            session.commit()
        else:
            # tutor = Tutor.get_from_kwarg(session, tutor_id=tutor_data["id"])
            # tutor_date = dt.strptime(tutor_data["updated_at"], "%Y-%m-%dT%H:%M:%S.000Z")
            # difference = dt.now() - tutor_date
            # if difference.days == 0:
            Tutor.update(tutor, tutor_data)
            session.commit()
        update_tutor_subject_relationship(tutor, session)


def update_tutor_subject_relationship(tutor, session):
    with session as session:
        try:
            tutor_subjects = tutor.subjects.replace('{', '[')
            tutor_subjects = tutor_subjects.replace('}', ']')

            SRP = "SRP"
            SOP = "SOP"
            DHO = "DHO"
            Erhvervscase = "Erhvervscase"
            Proces = "Proces"
            PLS = "PLS"

            subjects_list = Subjects.return_objects_from_list(
                eval(tutor_subjects), session)
            tutor.subjects_relationship.extend(subjects_list)

        except AttributeError:
            subjects_list = Subjects.return_objects_from_list(
                tutor.subjects, session)
            tutor.subjects_relationship.extend(subjects_list)

        except Exception as e:
            print(tutor, e)

        session.commit()


if __name__ == "__main__":
    get_tutor_students()
    update_tutor_pickle()
    # Kør kun denne her funktion, hvis subjects skal opdateres i DB!
    populate_subjects_in_db()
