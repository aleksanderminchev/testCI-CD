import requests
import datetime
import pandas as pd
import time
import ast
from dateutil.relativedelta import relativedelta
from decouple import config
# Internal imports
from api.app import db
from api.utils.lessonspace import create_lesson_space

from models.user import User
from models.student import Student
from models.customer import Customer
from models.teacher import Teacher
from models.balance import Balance
from models.referral import Referral
from models.wagepayment import WagePayment
from models.lesson import Lesson
from models.high_school import HighSchool
from models.higher_education_institution import HigherEducationInstitution
from models.higher_education_programme import HigherEducationProgramme
from models.qualification import Qualification
from models.subjects import Subjects
from models.program import Program
from models.interest import Interest
from models.language import Language

api_key = config("TW_API")

headers = {
    'Authorization': f'Token token={api_key}',
    'Content-Type': 'application/json'
}


def work_student():
    print('Getting students...')

    # ACTIVE STUDENTS
    print("Getting active students...")
    page = 1
    url1 = f"https://api.teachworks.com/v1/students?per_page=50&page={page}&status=Active"
    payload = {}
    response1 = requests.request("GET", url1, headers=headers, data=payload)
    json_response = response1.json()

    # Normalize JSON data into a flat table structure
    excel_all_data = pd.json_normalize(json_response)

    while bool(json_response):
        time.sleep(1)
        page += 1
        url = f"https://api.teachworks.com/v1/students?per_page=50&page={page}&status=Active"
        response = requests.request("GET", url, headers=headers, data=payload)
        json_response = response.json()
        read_js = pd.json_normalize(json_response)

        # Append new data to existing dataframe
        excel_all_data = excel_all_data.append(read_js, ignore_index=True)

    # INACTIVE STUDENTS
    print("Getting inactive students...")
    page = 1
    url1 = f"https://api.teachworks.com/v1/students?per_page=50&page={page}&status=Inactive"
    payload = {}
    response1 = requests.request("GET", url1, headers=headers, data=payload)
    json_response = response1.json()

    # Normalize JSON data into a flat table structure
    excel_all_data = pd.json_normalize(json_response)

    # Continues to fetch and process additional pages of active student data until no more pages exist
    while bool(json_response):
        time.sleep(1)
        page += 1
        url = f"https://api.teachworks.com/v1/students?per_page=50&page={page}&status=Inactive"
        response = requests.request("GET", url, headers=headers, data=payload)
        json_response = response.json()
        read_js = pd.json_normalize(json_response)

        # Append new data to existing dataframe
        excel_all_data = excel_all_data.append(read_js, ignore_index=True)

    # Converts the DataFrame to a dictionary for easier processing
    dict_students = excel_all_data.to_dict()

    # Iterates over each student ID in the dictionary
    for i in range(0, len(dict_students['id'])):
        # DATA CLEARNING AND VALIDATION

        # Prepares phone number data for processing, adding the country code if necessary
        phone = dict_students['mobile_phone'][i] or ""
        if type(phone) == str:
            if not phone.startswith("+"):
                phone = "+45" + phone
        else:
            phone = ''

        print(dict_students['id'][i])

        # Gets student and customer if they already exists in the database
        student = Student.query.get(dict_students['id'][i])
        customer = Customer.query.get(
            dict_students['customer_id'][i])

        # If the student does not exist, we create a new one
        if student is None:
            # If customer exists then attach student with existing Customer
            if customer is not None:
                # If the student is individual and the customer already exists, we simply create a Student.
                if dict_students['student_type'][i] == 'individual':
                    student = Student(
                        id=dict_students['id'][i],
                        customer_id=dict_students['customer_id'][i],
                        status=dict_students['status'][i].lower(),
                        first_name=dict_students['first_name'][i],
                        last_name=dict_students['last_name'][i],
                        email=dict_students['email'][i].lower(),
                        student_type="independent",
                    )
                    db.session.add(student)
                    db.session.commit()
                # Else it is not an individual student, so we create a User account
                # Make sure that a user with same email does not already exist
                elif type(dict_students['email'][i]) == str and dict_students['email'][i] != "":
                    check_user = User.query.filter_by(
                        email=dict_students['email'][i].lower()).first()
                    # If user does not exist we create them
                    if check_user is None:
                        user = User(
                            first_name=dict_students['first_name'][i],
                            last_name=dict_students['last_name'][i],
                            email=dict_students['email'][i].lower(),
                            phone=phone,
                            password=''
                        )
                        db.session.add(user)
                        db.session.commit()

                        student = Student(
                            id=dict_students['id'][i],
                            customer_id=dict_students['customer_id'][i],
                            user_id=user.uid,
                            status=dict_students['status'][i].lower(),
                            first_name=dict_students['first_name'][i],
                            last_name=dict_students['last_name'][i],
                            email=dict_students['email'][i].lower(),
                            student_type=dict_students['student_type'][i],
                            created_at=dict_students['created_at'][i],
                            last_updated=dict_students['updated_at'][i],
                        )
                        db.session.add(student)
                        db.session.commit()

                    # Student email already exists as a User Account, but not as a student
                    else:
                        raise Exception("ERROR: Student email already exists")
                # Student does not have an email, so we create a student without a user account
                else:
                    student = Student(
                        id=dict_students['id'][i],
                        customer_id=dict_students['customer_id'][i],
                        status=dict_students['status'][i].lower(),
                        first_name=dict_students['first_name'][i],
                        last_name=dict_students['last_name'][i],
                        email=dict_students['email'][i].lower(),
                        student_type=dict_students['student_type'][i],
                        created_at=dict_students['created_at'][i],
                        last_updated=dict_students['updated_at'][i],
                    )
                    db.session.add(student)
                    db.session.commit()
            # CUSTOMER IS NONE
            else:
                raise Exception("ERROR: Customer does not exist.")
        # STUDENT ALREADY EXISTS and has been updated on TW since last update.
        elif student.last_updated <= datetime.datetime.strptime(dict_students['updated_at'][i], "%Y-%m-%dT%H:%M:%S.000Z"):
            student_type = dict_students['student_type'][i]
            if dict_students['student_type'][i] == 'individual':
                student_type = 'independent'
            student.last_updated = dict_students['updated_at'][i]
            student.student_type = student_type
            student.first_name = dict_students['first_name'][i]
            student.last_name = dict_students['last_name'][i]
            student.status = dict_students['status'][i].lower()
            student.phone = phone
            if student.user is not None:
                student.phone = phone
                student.user.first_name = dict_students['first_name'][i]
                student.user.last_name = dict_students['last_name'][i]
            db.session.commit()


def work_customer():
    print('Getting customers...')

    # ACTIVE CUSTOMERS
    print("Getting active customers...")
    page = 1
    url1 = f"https://api.teachworks.com/v1/customers?per_page=50&page={page}&status=Active"
    payload = {}
    response1 = requests.request("GET", url1, headers=headers, data=payload)
    json_response = response1.json()

    # Normalize JSON data into a flat table structure
    excel_all_data = pd.json_normalize(json_response)

    # Keep making API calls until no more data is returned
    while bool(json_response):
        # Wait 1 second between requests to not overwhelm the API rate limit
        time.sleep(1)
        page += 1
        url = f"https://api.teachworks.com/v1/customers?per_page=50&page={page}&status=Active"
        response = requests.request("GET", url, headers=headers, data=payload)
        json_response = response.json()
        read_js = pd.json_normalize(json_response)

        # Append new data to existing dataframe
        excel_all_data = excel_all_data.append(read_js, ignore_index=True)

    # INACTIVE CUSTOMERS
    print("getting inactive customers...")
    page = 1
    url1 = f"https://api.teachworks.com/v1/customers?per_page=50&page={page}&status=Inactive"
    payload = {}
    response1 = requests.request("GET", url1, headers=headers, data=payload)
    json_response = response1.json()

    while bool(json_response):
        # Wait 1 second between requests to not overwhelm the API rate limit
        time.sleep(1)
        page += 1
        url = f"https://api.teachworks.com/v1/customers?per_page=50&page={page}&status=Inactive"
        response = requests.request("GET", url, headers=headers, data=payload)
        json_response = response.json()
        read_js = pd.json_normalize(json_response)

        # Append new data to existing dataframe
        excel_all_data = excel_all_data.append(read_js, ignore_index=True)

    dict_customers = excel_all_data.to_dict()

    for i in range(0, len(dict_customers['id'])):
        # DATA CLEARNING AND VALIDATION
        status = dict_customers['status'][i].lower()
        phone = dict_customers['mobile_phone'][i] or ""
        if type(phone) == str:
            if not phone.startswith("+"):
                phone = "+45" + phone
        else:
            phone = '+453214'
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

        # IF CUSTOMER EXISTS UPDATE CUSTOMER
        customer = Customer.query.get(dict_customers['id'][i])
        if customer is None:
            # Check if customer email exists then
            if type(dict_customers['email'][i]) == str:
                customer = User.query.filter_by(
                    email=dict_customers['email'][i].lower()).first()

        # If user email and ID does not exist then we create a new Customer with a User account.
        if customer is None:
            user = User(
                first_name=dict_customers['first_name'][i],
                last_name=dict_customers['last_name'][i],
                email=dict_customers['email'][i].lower(),
                phone=phone,
                password=''
            )
            db.session.add(user)
            db.session.commit()

            customer = Customer(
                id=dict_customers['id'][i],
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
            balance = Balance(
                customer_id=dict_customers['id'][i],
                hours_scheduled=0,
                hours_used=0,
                hours_free=0,
                hours_ordered=0,
                invoice_balance=0,
                currency='DKK')
            db.session.add(balance)
            db.session.commit()
        else:
            if customer.last_updated <= datetime.datetime.strptime(dict_customers['updated_at'][i], "%Y-%m-%dT%H:%M:%S.000Z"):
                customer.user.first_name = dict_customers['first_name'][i]
                customer.user.last_name = dict_customers['last_name'][i]
                customer.phone = phone
                customer.status = dict_customers['status'][i].lower()
                customer.last_updated = dict_customers['updated_at'][i]
                customer.email_lesson_notes = email_lesson_notes
                customer.email_lesson_reminder = email_lesson_reminders
                customer.stripe_id = stripe_id
                customer.customer_type = customer_type
                db.session.commit()


def work_lesson():
    print('Getting lessons...')
    today = datetime.datetime.now()
    upper_date = today + relativedelta(months=+2)
    upper_date = upper_date.strftime('%Y-%m-%d')
    lower_date = today + relativedelta(months=-1)
    lower_date = today.replace(day=16).strftime('%Y-%m-%d')

    url1 = f"https://api.teachworks.com/v1/lessons?per_page=50&page={1}&from_date>={lower_date}&from_date<={upper_date}"
    payload = {}
    response1 = requests.request("GET", url1, headers=headers, data=payload)
    json_response = response1.json()
    excel_all_data = pd.json_normalize(json_response)
    a = range(1, 55)

    for i in a:
        time.sleep(1)
        i_request = i + 1
        url = f"https://api.teachworks.com/v1/lessons?per_page=50&page={i_request}&from_date>={lower_date}&from_date<={upper_date}"
        response = requests.request("GET", url, headers=headers, data=payload)
        json_response = response.json()
        read_js = pd.json_normalize(json_response)
        excel_all_data = excel_all_data.append(read_js, ignore_index=True)

    dict_lessons = excel_all_data.to_dict()

    for i in range(0, len(dict_lessons['id'])):
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
        if dict_lessons['service_name'][i] == 'Opstartstid' \
                or dict_lessons['service_name'][i] == 'Opstartstid (universitetsniveau)' \
                or dict_lessons['service_name'][i] == 'Opstartsmøde':
            trial_lesson = True
        description = dict_lessons['description'][i]
        if type(description) != str:
            description = ''
        lesson_check = Lesson.query.get(dict_lessons['id'][i])
        if lesson_check is None:
            employee_id = dict_lessons['employee_id'][i]

            teacher = Teacher.query.filter_by(
                teachworks=str(employee_id)).first()
            if teacher is not None:
                teacher_id = teacher.id
                id = dict_lessons['id'][i]
                from_time = dict_lessons['from_datetime'][i]
                to_time = dict_lessons['to_datetime'][i]
                duration_in_minutes = dict_lessons['duration_minutes'][i]
                created_at = dict_lessons['created_at'][i]
                completed_at = dict_lessons['completed_at'][i]
                if type(completed_at) != str:
                    completed_at = datetime.datetime.now()
                updated_at = dict_lessons['updated_at'][i]
                wage = dict_lessons['wage'][i]
                title = ''
                completion_notes = ''
                student_data = ast.literal_eval(
                    dict_lessons['participants'][i])
                space_id = ''
                secret = ''
                space = ''
                session_id = ''
                for j in student_data:
                    student_id = j['student_id']
                    student = Student.query.filter_by(
                        id=student_id).first()
                    if student is not None:
                        title = f'Lesson with {student.first_name} {student.last_name}'
                        completion_notes = j['public_notes']
                        if completion_notes is None:
                            completion_notes = ''
                        lesson_reminder_sent_at = j['student_reminder_sent_at']
                        if lesson_reminder_sent_at is None:
                            lesson_reminder_sent_at = datetime.datetime.now()
                paid = False
                wage_id = dict_lessons['wage_payment_id'][i]
                lesson_url = create_lesson_space(teacher, j)
                space_id = lesson_url['room_id']
                secret = lesson_url['secret']
                session_id = lesson_url['session_id']
                space = lesson_url['space']
                if isinstance(wage_id, (int, float, complex)):
                    paid = True
                lesson = Lesson(id=id, teacher_id=teacher_id,
                                title=title,
                                description=description,
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
                                space=space,
                                space_id=space_id,
                                secret=secret,
                                session_id=session_id,
                                paid=paid)
                db.session.add(lesson)
                db.session.commit()
            for j in student_data:
                student = Student.query.filter_by(
                    id=j['student_id']).first()
                if student is not None:
                    student.lessons.append(lesson)
                    duration = round(lesson.duration_in_minutes / 60, 2)
                    if not lesson.trial_lesson:
                        if student.customer is not None:
                            if lesson.status.value == 'scheduled':
                                student.customer.balance[0].hours_scheduled += duration
                            elif lesson.status.value == 'attended':
                                student.customer.balance[0].hours_used += duration
                            elif lesson.status.value == 'bad cancellation student':
                                if duration > 2:
                                    student.customer.customer.balance[0].hours_used += 2
                                else:
                                    student.customer.customer.balance[0].hours_used += duration
                db.session.commit()
            else:
                if lesson_check.last_updated <= datetime.datetime.strptime(dict_lessons['updated_at'][i], "%Y-%m-%dT%H:%M:%S.000Z"):
                    lesson_check.teacher_id = dict_lessons['employee_id'][i]
                    lesson_check.created_at = dict_lessons['created_at'][i]
                    lesson_check.last_updated = dict_lessons['updated_at'][i]
                    completed_at = dict_lessons['completed_at'][i]
                    paid = False
                    wage_id = dict_lessons['wage_payment_id'][i]
                    if isinstance(wage_id, (int, float, complex)):
                        paid = True
                    if type(completed_at) != str:
                        completed_at = datetime.datetime.now()
                    lesson_check.paid = paid
                    lesson_check.completed_at = completed_at
                    lesson_check.description = description
                    lesson_check.from_time = dict_lessons['from_datetime'][i]
                    lesson_check.to_time = dict_lessons['to_datetime'][i]
                    lesson_check.trial_lesson = trial_lesson
                    lesson_check.description = description
                    lesson_check.wage = dict_lessons['wage'][i]
                    duration_new = round(
                        dict_lessons['duration_minutes'][i] / 60, 2)
                    duration_old = round(
                        lesson_check.duration_in_minutes / 60, 2)
                    student_data = ast.literal_eval(
                        dict_lessons['participants'][i])
                    students = []
                    title = ''
                    completion_notes = ''
                    lesson_reminder_sent_at = datetime.datetime.now()
                    for j in student_data:
                        student = Student.query.get(j['student_id'])
                        if student is not None:
                            title = f'Lesson with {student.first_name} {student.last_name}'
                            students.append(student)
                            completion_notes = j['public_notes']
                            if completion_notes is None:
                                completion_notes = ''
                            lesson_reminder_sent_at = j['student_reminder_sent_at']
                            if lesson_reminder_sent_at is None:
                                lesson_reminder_sent_at = datetime.datetime.now()
                            if not lesson_check.trial_lesson:
                                if student.customer is not None:
                                    # old status remove hours
                                    if lesson_check.status.value == 'scheduled':
                                        student.customer.balance[0].hours_scheduled -= duration_old
                                    elif lesson_check.status.value == 'attended':
                                        student.customer.balance[0].hours_used -= duration_old
                                    elif lesson_check.status.value == 'bad cancellation student':
                                        print('cancelled')
                                        if duration_old > 2:
                                            student.customer.balance[0].hours_used -= 2
                                        else:
                                            student.customer.balance[0].hours_used -= duration_old
                                    # New status add hours
                                    if status == 'scheduled':
                                        student.customer.balance[0].hours_scheduled += duration_new
                                    elif status == 'attended':
                                        student.customer.balance[0].hours_used += duration_new
                                    elif status == 'bad cancellation student':
                                        print('cancelled')
                                        if duration_new > 2:
                                            student.customer.balance[0].hours_used += 2
                                        else:
                                            student.customer.balance[0].hours_used += duration_new

                lesson_check.status = status
                lesson_check.lessons_students = students
                lesson_check.title = title
                lesson_check.duration_in_minutes = duration_new
                lesson_check.completion_notes = completion_notes
                lesson_check.lesson_reminder_sent_at = lesson_reminder_sent_at

            db.session.commit()
            print('Finished getting lessons.')


def work_teachers():
    """ Fetches data from an TW API and updates the database with teacher information """
    print('work teachers')

    # Set up first API call to retrieve first page of data
    url1 = f"https://api.teachworks.com/v1/employees?per_page=50&page={1}"
    payload = {}
    response1 = requests.request("GET", url1, headers=headers, data=payload)
    json_response = response1.json()

    # Normalize JSON data into a flat table structure
    excel_all_data = pd.json_normalize(json_response)
    page = 1

    # Keep making API calls until no more data is returned
    while bool(json_response):
        # Wait 1 second between requests to not overwhelm the API rate limit
        time.sleep(1)
        page += 1
        url = f"https://api.teachworks.com/v1/employees?per_page=50&page={page}"
        response = requests.request("GET", url, headers=headers, data=payload)
        json_response = response.json()
        read_js = pd.json_normalize(json_response)

        # Append new data to existing dataframe
        excel_all_data = excel_all_data.append(read_js, ignore_index=True)

    # Filter the dataframe to only include the 'id' and 'custom_fields' columns
    new = excel_all_data.filter(['id', 'custom_fields'], axis=1)

    # Initialize an empty dataframe to store the transformed custom fields
    test = pd.DataFrame()

    # For each row, transform 'custom_fields' from list of dicts to individual columns
    for i in range(0, len(new['id'])):
        temp_df = pd.DataFrame()
        for j in new['custom_fields'][i]:
            a = list()
            value = ' '
            if j['value'] is not None:
                value = j['value']
            a.append(value)
            temp_df[j['name']] = a
        # Append transformed data to 'test' dataframe
        test = test.append(temp_df, ignore_index=True)

    # Merge 'test' dataframe with original data
    new = new.merge(test, right_index=True, left_index=True)
    excel_all_data = excel_all_data.merge(
        new, right_index=True, left_index=True)

    # Convert the final dataframe to a dictionary
    dict_teachers = excel_all_data.to_dict()

    # Iterate through each teacher's data
    for i in range(0, len(dict_teachers['id_x'])):
        # Various data cleaning and validation steps are performed here

        # Validating the email
        if type(dict_teachers["email"][i]) == str:
            email = dict_teachers["email"][i].lower()
            if email == "":
                continue  # if no email then just continue and skip this teacher
        else:
            continue  # if no email then just continue and skip this teacher

        first_name = dict_teachers["first_name"][i]
        last_name = dict_teachers["last_name"][i]

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
            local_store = payroll_id[0:6] + "-" + payroll_id[6:]
            payroll_id = local_store

        # Setting default values
        reg_and_bank_digits = ''
        bank_number = ""
        reg_number = ""
        # Only get the digits
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
        gender = 'female'
        if dict_teachers["Køn"][i] == 'Mand':
            gender = 'male'

        # If empty string then make it Null
        birthday = dict_teachers["birth_date"][i]
        if birthday == "":
            birthday = None

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
        print(programs)
        # Assign the Program instances to the Teacher instance

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
            lang = Language.query.filter_by(name=name).first()
            if not lang:
                raise NameError("LANGUAGE NAME DOES NOT EXIST ", name)

            langs.append(lang)
        # Assign the Language instances to the Teacher instance

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
                raise NameError(
                    "qualification NAME DOES NOT EXIST ", name)

            qualifications.append(qualification)

        # Assign the Program instances to the Teacher instance
        name = ''
        # Add higher education programme
        if type(dict_teachers["Hvis du går på en videregående uddannelse. Hvilken uddannelse læser du så på?"][i]) == str:
            name = dict_teachers["Hvis du går på en videregående uddannelse. Hvilken uddannelse læser du så på?"][i]
        higher_education_program = HigherEducationProgramme.query.filter_by(
            name=name).first()

        name = ''
        # Add higher education institution
        if type(dict_teachers["Videregående uddannelsesinstitution"][i]) == str:
            name = dict_teachers["Videregående uddannelsesinstitution"][i]
        higher_education_institution = HigherEducationInstitution.query.filter_by(
            name=name).first()
        name = ''
        if type(dict_teachers["Gymnasietype "][i]) == str:
            name = dict_teachers["Gymnasietype "][i]
        # Add high school
        high_school = HighSchool.query.filter_by(name=name).first()

        # If teacher email does not exist in database, add them
        teacher_check = User.query.filter_by(email=email).first()
        if teacher_check is None:
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

            db.session.add(teacher)
            db.session.commit()
            teacher.subjects = subjects
            teacher.programs = programs
            teacher.languages = langs
            teacher.interests = interests
            teacher.qualifications = qualifications
            if higher_education_program is not None:
                teacher.higher_education_programmes = [
                    higher_education_program]
            if higher_education_institution is not None:
                teacher.higher_education_institutions = [
                    higher_education_institution]
            if high_school is not None:
                teacher.high_school = [high_school]

            db.session.commit()
            print(first_name, " ", last_name, " successfully added")
        # Else teacher already exists, so we update the teacher instead
        else:
            teacher_check = teacher_check.teacher
            if teacher_check.last_updated <= datetime.datetime.strptime(dict_teachers['updated_at'][i], "%Y-%m-%dT%H:%M:%S.000Z"):
                teacher_check.user.first_name = first_name
                teacher_check.user.last_name = last_name
                teacher_check.user.phone = phone
                teacher_check.wage_per_hour = 150
                teacher_check.bio = dict_teachers["bio"][i]
                teacher_check.status = dict_teachers["status"][i].lower()
                teacher_check.country = dict_teachers["country"][i] or "Denmark"
                teacher_check.address = dict_teachers["address"][i]
                teacher_check.city = dict_teachers["city"][i]
                teacher_check.zip_code = dict_teachers["zip"][i]
                teacher_check.gender = gender
                teacher_check.photo = photo
                teacher_check.created_on_tw_at = dict_teachers["created_at"][i]
                teacher_check.updated_on_tw_at = dict_teachers["updated_at"][i]
                teacher_check.created_at = dict_teachers["created_at"][i]
                teacher_check.last_updated = dict_teachers["updated_at"][i]
                teacher_check.open_for_new_students = open_for_new_students
                teacher_check.birthday = birthday
                teacher_check.bank_number = bank_number
                teacher_check.reg_number = reg_number
                teacher_check.teachworks = dict_teachers["id_x"][i]
                teacher_check.payroll_id = payroll_id
                teacher_check.grade_average = grade_average
                teacher_check.internal_note = dict_teachers["Intern note"][i]
                teacher_check.how_they_found = dict_teachers["Hvor har du hørt om os? "][i]
                teacher_check.finished_highschool = finished_highschool,
                teacher_check.inactive_reason = dict_teachers["Grund til tutor stopper "][i]
                teacher_check.application_reason = dict_teachers[
                    "Hvorfor valgte du at ansøge hos TopTutors?"][i]
                if len(subjects) != 0:
                    teacher_check.subjects = subjects
                db.session.commit()
                if len(programs) != 0:
                    teacher_check.programs = programs
                db.session.commit()
                if len(langs) != 0:
                    teacher_check.languages = langs
                db.session.commit()
                if len(interests) != 0:
                    teacher_check.interests = interests
                db.session.commit()
                if len(qualifications) != 0:
                    teacher_check.qualifications = qualifications
                if higher_education_program is not None:
                    teacher_check.higher_education_programmes = [
                        higher_education_program]
                if higher_education_institution is not None:
                    teacher_check.higher_education_institutions = [
                        higher_education_institution]
                if high_school is not None:
                    teacher_check.high_school = [high_school]
        print("All tutors have been added")


def work_payslips():
    print('Getting payslips...')

    api_key = config("TW_API")
    headers = {
        'Authorization': f'Token token={api_key}',
        'Content-Type': 'application/json'
    }
    today = datetime.datetime.now()

    if today.day >= 16:
        lower_date = today.replace(day=16).strftime('%Y-%m-%d')
        upper_date = today + relativedelta(months=+1)
        upper_date = upper_date.replace(day=15).strftime('%Y-%m-%d')
    else:
        upper_date = today.replace(day=15).strftime('%Y-%m-%d')
        lower_date = today + relativedelta(months=-1)
        lower_date = today.replace(day=16).strftime('%Y-%m-%d')

    url_lessons = f"https://api.teachworks.com/v1/lessons?per_page=50&page={1}&from_date>={lower_date}&to_date<={upper_date}"
    payload = {}
    response1 = requests.request(
        "GET", url_lessons, headers=headers, data=payload)
    json_response = response1.json()
    df_lessons = pd.json_normalize(json_response)
    a = range(1, 55)

    for i in a:
        time.sleep(1)
        i_request = i+1
        url_lesson = f"https://api.teachworks.com/v1/lessons?per_page=50&page={i_request}&from_date>={lower_date}&to_date<={upper_date}"
        response = requests.request(
            "GET", url_lesson, headers=headers, data=payload)
        json_response = response.json()
        read_js = pd.json_normalize(json_response)
        df_lessons = df_lessons.append(read_js, ignore_index=True)

    url1 = f"https://api.teachworks.com/v1/wage_payments?per_page=50&page={1}&from_date>={lower_date}&to_date<={upper_date}"
    url_copensation = f"https://api.teachworks.com/v1/other_compensation?per_page=50&page={1}&from_date>={lower_date}&to_date<={upper_date}"
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
        url = f"https://api.teachworks.com/v1/wage_payments?per_page=50&page={i_request}&from_date>={lower_date}&to_date<={upper_date}"
        response = requests.request("GET", url, headers=headers, data=payload)
        json_response = response.json()
        print(response)
        read_js = pd.json_normalize(json_response)
        excel_all_data = excel_all_data.append(read_js, ignore_index=True)
        print(excel_all_data)

    for j in b:
        time.sleep(1)
        i_request = j+1
        url = f"https://api.teachworks.com/v1/other_compensation?per_page=50&page={i_request}&from_date>={lower_date}&to_date<={upper_date}"
        response = requests.request("GET", url, headers=headers, data=payload)
        json_response = response.json()
        print(response)
        read_js = pd.json_normalize(json_response)
        other_comp_excell = other_comp_excell.append(
            read_js, ignore_index=True)
        print(other_comp_excell)

    dict_lessons = df_lessons.to_dict()
    dict_wages = excel_all_data.to_dict()
    dict_referrals = other_comp_excell.to_dict()
    for i in range(0, len(dict_wages['id'])):
        wage_payment_check = WagePayment.query.get(dict_wages['id'][i])
        if wage_payment_check is None:
            teacher_id = dict_wages['employee_id'][i]
            teacher = Teacher.query.filter_by(
                teachworks=str(teacher_id)).first()
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
                                          hours=round(hours / 60, 2),
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
    for i in range(0, len(dict_referrals['id'])):
        referral_check = Referral.query.get(dict_referrals['id'][i])
        if referral_check is None:
            wagepayment = WagePayment.query.filter_by(
                id=dict_referrals['wage_payment_id'][i]).first()
            if wagepayment is not None:
                teacher = Teacher.query.filter_by(teachworks=str(
                    dict_referrals['employee_id'][i])).first()
                if teacher is not None:
                    wagepayment.referrals_amount = dict_referrals['amount'][i]
                    wagepayment.referrals_number = dict_referrals['amount'][i] / 200
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
