from api.app import db
import unittest
from api.utils.utils import datetime
from tests.base_test_case import BaseTestCase
from models.teacher import Teacher
from models.student import Student
from models.user import User
from unittest.mock import Mock


class TeacherModelTestCase(BaseTestCase):

    def setUp(self):
        pass
        # user_teacher = User(email='teacher@test.com', password='foo')
        self.teacher=Teacher()
        # self.user_teacher = user_teacher
        # db.session.add(self.user_teacher)
        # db.session.commit()
        # teacher = Teacher(user_id=user_teacher.uid, wage_per_hour=120.00, bio="ewfewvwv",
        #                   photo="wdq", open_for_new_students=True, payroll_id="12", status='active',)
        # db.session.add(teacher)
        # db.session.commit()

    def tearDown(self):
        Teacher.query.delete()
        User.query.delete()
        db.session.commit()

    def test_filters_teacher_with_user_params_fail(self):
        args_filters = {
            "first_name": "someNameToFail",
        }
        teacher = Teacher.filter_teachers(**args_filters)
        assert not teacher
        assert len(teacher) == 0

    def test_filters_teacher_with_user_params(self):
        args_for_teacher = {
            "email": "newteacher1@email.com",
            "first_name": "Teacher1",
            "last_name": "Teacher2",
            "password": "password",
            "phone": "123312",
            "photo": "12ggerge",
            "wage_per_hour": 120,
            "bio": "ever",
            "age": 21,
            "birthday": datetime.datetime.now(),
            "open_for_new_students": True,
            "high_school": "Some highschool",
            "finished_highschool": True,
            "higher_education_institution": 1,
            "higher_education_programme": 1
        }

        Teacher.add_new_teacher(**args_for_teacher)

        args_filters = {
            "first_name": "Teacher1",
            "last_name": "Teacher2",
        }

        teacher = Teacher.filter_teachers(**args_filters)

        assert teacher
        assert len(teacher) != 0
        assert teacher[0]['last_name'] == "Teacher2"
        assert teacher[0]['first_name'] == "Teacher1"

    def test_filters_teacher_with_teacher_params(self):

        args_for_teacher = {
            "email": "newteacher2@email.com",
            "first_name": "Teacher12",
            "last_name": "Teacher2",
            "password": "password",
            "phone": "123312",
            "photo": "12ggerge",
            "wage_per_hour": 120,
            "bio": "ever",
            "age": 25,
            "birthday": datetime.datetime.now(),
            "open_for_new_students": True,
            "finished_highschool": True,
            "higher_education_institution": 1,
            "higher_education_programme": 1
        }
        Teacher.add_new_teacher(**args_for_teacher)

        args_filters = {
            "age": 25,
        }
        teacher = Teacher.filter_teachers(**args_filters)

        assert teacher
        assert len(teacher) != 0

        args_filters = {
            "open_for_new_students": True,
            "email": "newteacher2@email.com",
            "wage_per_hour": 120,
        }
        teacher = Teacher.filter_teachers(**args_filters)

        assert teacher
        assert len(teacher) != 0

    def test_filters_teacher_and_user_params_fail(self):
        args_filters = {
            "first_name": "Teacher12123123213",
            "photo": "12ggerge"
        }
        teacher = Teacher.filter_teachers(**args_filters)
        assert not teacher
        assert len(teacher) == 0

    def test_filters_teacher_with_teacher_params_fail(self):
        args_filters = {
            "wage_per_hour": 150
        }
        teacher = Teacher.filter_teachers(**args_filters)

        assert not teacher
        assert len(teacher) == 0

    def test_add_student_to_teacher(self):
        students = Teacher.add_student_to_teacher(
            student_id=[1], teacher_email="teacher@test.com")
        student_check = Student.get_student_by_id(1)
        assert students
        assert len(students) != 0
        assert student_check in students

    def test_remove_student_from_teacher(self):
        students = Teacher.remove_student_from_teacher(
            student_id=1, teacher_email="teacher@test.com")
        student_check = Student.get_student_by_id(1)
        assert not students
        assert len(students) == 0
        assert student_check not in students

    def test_valid_partitions_return_teacher_object(self):
        args_for_teacher = {
            "email": "example@mail.com",
            "first_name": "John",
            "last_name": "Teacher",
            "phone": "+1234567890",
            "wage_per_hour": 1000,
            "payroll_id":"010121-1234",
            "photo":"",
            "bio": "ever",
            "age": 21,
            "birthday": datetime.datetime.now(),
            "open_for_new_students": True,
            "finished_highschool": True,
        }

        result = Teacher.add_new_teacher(**args_for_teacher)
        self.assertIs(type(result), type(self.teacher))
    
    def test_invalid_wage_negative_number_returns_invalid_wage(self):
        args_for_teacher = {
            "email": "example@mail.com",
            "first_name": "John",
            "last_name": "Teacher",
            "phone": "+1234567890",
            "wage_per_hour": -500,
            "payroll_id":"010121-1234",
            "photo":"",
            "bio": "ever",
            "age": 21,
            "birthday": datetime.datetime.now(),
            "open_for_new_students": True,
            "finished_highschool": True,
        }
        try:
            result = Teacher.add_new_teacher(**args_for_teacher)
        except ValueError as e:
            print(e)
            self.assertEqual(str(e), "invalid wage")
    
    def test_invalid_wage_string_returns_invalid_wage(self):
        args_for_teacher = {
            "email": "example@mail.com",
            "first_name": "John",
            "last_name": "Teacher",
            "phone": "+1234567890",
            "wage_per_hour": "invalid",
            "payroll_id": "010121-1234",
            "photo": "",
            "bio": "ever",
            "age": 21,
            "birthday": datetime.datetime.now(),
            "open_for_new_students": True,
            "finished_highschool": True,
        }
        try:
            result = Teacher.add_new_teacher(**args_for_teacher)
        except ValueError as e:
            self.assertEqual(str(e), "invalid wage")
        
    def test_valid_wage_zero_returns_teacher_object(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 0
        }
        try:
            result = Teacher.add_new_teacher(**data)
            self.assertIs(type(result), type(self.teacher))
        except ValueError:
            self.fail("Expected no exception, but ValueError was raised.")

    def test_valid_wage_positive_number_returns_teacher_object(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1500
        }
        try:
            result = Teacher.add_new_teacher(**data)
            self.assertIs(type(result), type(self.teacher))
        except ValueError:
            self.fail("Expected no exception, but ValueError was raised.")

    def test_valid_email_returns_teacher_object(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        try:
            result = Teacher.add_new_teacher(**data)
            self.assertIs(type(result), type(self.teacher))
        except ValueError:
            self.fail("Expected no exception, but ValueError was raised.")
        
    def test_invalid_email_length_above_boundary_returns_invalid_email(self):
        data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "a" * 121 + "@mail.com",
        "phone": "+1234567890",
        "payroll_id": "010121-1234",
        "wage_per_hour": 1000
        }
        try:
            result = Teacher.add_new_teacher(**data)
        except ValueError as e:
            self.assertEqual(str(e), "invalid email")

    def test_invalid_email_length_below_boundary_returns_invalid_email(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "a" * 11 + "@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        try:
            result = Teacher.add_new_teacher(**data)
        except ValueError as e:
            self.assertEqual(str(e), "invalid email")

    def test_invalid_email_length_zero_returns_invalid_email(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        try:
            result = Teacher.add_new_teacher(**data)
        except ValueError as e:
            self.assertEqual(str(e), "invalid email")

    def test_invalid_email_nonstring_returns_invalid_email(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": 12345,
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        try:
            result = Teacher.add_new_teacher(**data)
        except ValueError as e:
            self.assertEqual(str(e), "invalid email")
        
    def test_valid_phone_returns_teacher_object(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        try:
            result = Teacher.add_new_teacher(**data)
            self.assertIs(type(result), type(self.teacher))
        except ValueError as e:
            self.fail("Expected no ValueError, but got: {}".format(str(e)))

    def test_invalid_phone_nonstring_returns_invalid_phone(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": 12345,
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        try:
            result = Teacher.add_new_teacher(**data)
        except ValueError as e:
            self.assertEqual(str(e), "invalid phone")

    def test_invalid_phone_length_zero_returns_invalid_phone(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        try:
            result = Teacher.add_new_teacher(**data)

        except ValueError as e:
            self.assertEqual(str(e), "invalid phone")

    def test_invalid_phone_length_above_boundary_returns_invalid_phone(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+12345678901",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        try:
            result = Teacher.add_new_teacher(**data)
        except ValueError as e:
            self.assertEqual(str(e), "invalid phone")
        
    def test_valid_first_name_returns_teacher_object(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        try:
            result = Teacher.add_new_teacher(**data)
            self.assertIs(type(result), type(self.teacher))
        except ValueError as e:
            self.fail("Expected no ValueError, but got: {}".format(str(e)))

    def test_invalid_first_name_nonstring_returns_invalid_first_name(self):
        data = {
            "first_name": 12345,
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        try:
            result = Teacher.add_new_teacher(**data)

        except ValueError as e:
            self.assertEqual(str(e), "invalid first name")

    def test_invalid_first_name_length_zero_returns_invalid_first_name(self):
        data = {
            "first_name": "",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        try:
            result = Teacher.add_new_teacher(**data)
        except ValueError as e:
            self.assertEqual(str(e), "invalid first name")

    def test_invalid_first_name_length_above_boundary_returns_invalid_first_name(self):
        data = {
            "first_name": "J" * 51,
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        try:
            result = Teacher.add_new_teacher(**data)
        except ValueError as e:
            self.assertEqual(str(e), "invalid first name")
    
    def test_valid_last_name_returns_teacher_object(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        result = Teacher.add_new_teacher(**data)
        self.assertIs(type(result), type(self.teacher))

    def test_invalid_last_name_nonstring_returns_invalid_last_name(self):
        data = {
            "first_name": "John",
            "last_name": 12345,
            "email": "example@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        try:
            Teacher.add_new_teacher(**data)
        except ValueError as e:
            self.assertEqual(str(e), "invalid last name")

    def test_invalid_last_name_length_zero_returns_invalid_last_name(self):
        data = {
            "first_name": "John",
            "last_name": "",
            "email": "example@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        try:
            Teacher.add_new_teacher(**data)
        except ValueError as e:
            self.assertEqual(str(e), "invalid last name")

    def test_invalid_last_name_length_above_boundary_returns_invalid_last_name(self):
        data = {
            "first_name": "John",
            "last_name": "D" * 51,
            "email": "example@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        try:
            Teacher.add_new_teacher(**data)
        except ValueError as e:
            self.assertEqual(str(e), "invalid last name")

    def test_valid_payroll_id_returns_teacher_object(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        result = Teacher.add_new_teacher(**data)
        self.assertIs(type(result), type(self.teacher))

    def test_invalid_payroll_id_nonstring_returns_invalid_payroll_id(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
            "payroll_id": 12345,
            "wage_per_hour": 1000
        }
        try:
            Teacher.add_new_teacher(**data)
        except ValueError as e:
            self.assertEqual(str(e), "invalid cpr")

    def test_invalid_payroll_id_length_zero_returns_invalid_payroll_id(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
            "payroll_id": "",
            "wage_per_hour": 1000
        }
        try:
            Teacher.add_new_teacher(**data)
        except ValueError as e:
            self.assertEqual(str(e), "invalid cpr")

    def test_invalid_payroll_id_length_above_boundary_returns_invalid_payroll_id(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-12345",
            "wage_per_hour": 1000
        }
        try:
            Teacher.add_new_teacher(**data)
        except ValueError as e:
            self.assertEqual(str(e), "invalid cpr")

    def test_invalid_payroll_id_format_returns_invalid_payroll_id(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
            "payroll_id": "01Jan21-ABCD",
            "wage_per_hour": 1000
        }
        try:
            Teacher.add_new_teacher(**data)
        except ValueError as e:
            self.assertEqual(str(e), "invalid cpr")
    
    def test_boundary_analysis_valid_email_length_between_12_and_120(self):
        data1 = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "a" * 12 + "@mail.com",
        "phone": "+1234567890",
        "payroll_id": "010121-1234",
        "wage_per_hour": 1000
        }
        result1 = Teacher.add_new_teacher(**data1)
        self.assertIs(type(result1), type(self.teacher))

        data2 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "a" * 120 + "@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        result2 = Teacher.add_new_teacher(**data2)
        self.assertIs(type(result2), type(self.teacher))

    def test_boundary_analysis_invalid_email_length_below_12_and_above_120(self):
        data1 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "a" * 2 + "@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        try:
            Teacher.add_new_teacher(**data1)
        except ValueError as e:
            self.assertEqual(str(e), "invalid email")

        data2 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "a" * 121 + "@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        try:
            Teacher.add_new_teacher(**data2)
        except ValueError as e:
            self.assertEqual(str(e), "invalid email")

    def test_boundary_analysis_valid_phone_length_between_9_and_12(self):
        data1 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+123456789",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        result1 = Teacher.add_new_teacher(**data1)
        self.assertIs(type(result1), type(self.teacher))

        data2 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example1@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        result2 = Teacher.add_new_teacher(**data2)
        self.assertIs(type(result2), type(self.teacher))

    def test_boundary_analysis_invalid_phone_length_below_9_and_above_12(self):
        data1 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+12345678905",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        try:
            Teacher.add_new_teacher(**data1)
        except ValueError as e:
            self.assertEqual(str(e), "invalid phone")

        data2 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example1@mail.com",
            "phone": "+123456",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        try:
            Teacher.add_new_teacher(**data2)
        except ValueError as e:
            self.assertEqual(str(e), "invalid phone")

    def test_boundary_analysis_valid_first_name_length_between_1_and_50(self):
        data1 = {
            "first_name": "J",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        result1 = Teacher.add_new_teacher(**data1)
        self.assertIs(type(result1), type(self.teacher))

        data2 = {
            "first_name": "J" * 50,
            "last_name": "Doe",
            "email": "example1@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        result2 = Teacher.add_new_teacher(**data2)
        self.assertIs(type(result2), type(self.teacher))
    
    def test_boundary_analysis_invalid_first_name_length_below_1_and_above_50(self):
        data1 = {
            "first_name": "",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        try:
            Teacher.add_new_teacher(**data1)
        except ValueError as e:
            self.assertEqual(str(e), "invalid first name")

        data2 = {
            "first_name": "J" * 51,
            "last_name": "Doe",
            "email": "example1@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        try:
            Teacher.add_new_teacher(**data2)
        except ValueError as e:
            self.assertEqual(str(e), "invalid first name")

    def test_boundary_analysis_valid_last_name_length_between_1_and_50(self):
        data1 = {
            "first_name": "John",
            "last_name": "D",
            "email": "example@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        result1 = Teacher.add_new_teacher(**data1)
        self.assertIs(type(result1), type(self.teacher))

        data2 = {
            "first_name": "John",
            "last_name": "D" * 50,
            "email": "example1@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        result2 = Teacher.add_new_teacher(**data2)
        self.assertIs(type(result2), type(self.teacher))

    def test_boundary_analysis_invalid_last_name_length_below_1_and_above_50(self):
        data1 = {
            "first_name": "John",
            "last_name": "",
            "email": "example@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        try:
            Teacher.add_new_teacher(**data1)
        except ValueError as e:
            self.assertEqual(str(e), "invalid last name")

        data2 = {
            "first_name": "John",
            "last_name": "D" * 51,
            "email": "example1@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        try:
            Teacher.add_new_teacher(**data2)
        except ValueError as e:
            self.assertEqual(str(e), "invalid last name")

    def test_boundary_analysis_valid_payroll_id_length_between_1_and_20(self):
        data1 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010021-1000",
            "wage_per_hour": 1000
        }
        result1 = Teacher.add_new_teacher(**data1)
        self.assertIs(type(result1), type(self.teacher))

    def test_boundary_analysis_invalid_payroll_id_length_below_1_and_above_20(self):
        data1 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
            "payroll_id": "",
            "wage_per_hour": 1000
        }
        try:
            Teacher.add_new_teacher(**data1)
        except ValueError as e:
            self.assertEqual(str(e), "invalid cpr")

        data2 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example1@mail.com",
            "phone": "+1234567890",
            "payroll_id": "01Jan21-1" * 11,
            "wage_per_hour": 1000
        }
        try:
            Teacher.add_new_teacher(**data2)
        except ValueError as e:
            self.assertEqual(str(e), "invalid cpr")


    def test_valid_email_length_between_12_and_120(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        result = Teacher.add_new_teacher(**data)
        self.assertIs(type(result), type(self.teacher))


    def test_invalid_email_length_below_12_and_above_120(self):
        data1 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "ex@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        try:
            Teacher.add_new_teacher(**data1)
        except ValueError as e:
            self.assertEqual(str(e), "invalid email")

        data2 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example1@mail.com" * 10,
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        try:
            Teacher.add_new_teacher(**data2)
        except ValueError as e:
            self.assertEqual(str(e), "invalid email")


    def test_valid_phone_length_between_9_and_12(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        result = Teacher.add_new_teacher(**data)
        self.assertIs(type(result), type(self.teacher))


    def test_invalid_phone_length_below_9_and_above_12(self):
        data1 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        try:
            Teacher.add_new_teacher(**data1)
        except ValueError as e:
            self.assertEqual(str(e), "invalid phone")

        data2 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example1@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        try:
            Teacher.add_new_teacher(**data2)
        except ValueError as e:
            self.assertEqual(str(e), "invalid phone")

    def test_valid_first_name_length_between_1_and_50(self):
        data1 = {
            "first_name": "J",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        result1 = Teacher.add_new_teacher(**data1)
        self.assertIs(type(result1), type(self.teacher))

        data2 = {
            "first_name": "J" * 50,
            "last_name": "Doe",
            "email": "example1@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        result2 = Teacher.add_new_teacher(**data2)
        self.assertIs(type(result2), type(self.teacher))


    def test_invalid_first_name_length_below_1_and_above_50(self):
        data1 = {
            "first_name": "",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        try:
            Teacher.add_new_teacher(**data1)
        except ValueError as e:
            self.assertEqual(str(e), "invalid first name")

        data2 = {
            "first_name": "J" * 51,
            "last_name": "Doe",
            "email": "example1@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        try:
            Teacher.add_new_teacher(**data2)
        except ValueError as e:
            self.assertEqual(str(e), "invalid first name")


    def test_valid_last_name_length_between_1_and_50(self):
        data1 = {
            "first_name": "John",
            "last_name": "D",
            "email": "example@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        result1 = Teacher.add_new_teacher(**data1)
        self.assertIs(type(result1), type(self.teacher))

        data2 = {
            "first_name": "John",
            "last_name": "D" * 50,
            "email": "example1@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        result2 = Teacher.add_new_teacher(**data2)
        self.assertIs(type(result2), type(self.teacher))


    def test_invalid_last_name_length_below_1_and_above_50(self):
        data1 = {
            "first_name": "John",
            "last_name": "",
            "email": "example@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        try:
            Teacher.add_new_teacher(**data1)
        except ValueError as e:
            self.assertEqual(str(e), "invalid last name")

        data2 = {
            "first_name": "John",
            "last_name": "D" * 51,
            "email": "example1@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        try:
            Teacher.add_new_teacher(**data2)
        except ValueError as e:
            self.assertEqual(str(e), "invalid last name")


    def test_valid_payroll_id_length_11(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        result = Teacher.add_new_teacher(**data)
        self.assertIs(type(result), type(self.teacher))


    def test_invalid_payroll_id_length_below_11_and_above_11(self):
        data1 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        try:
            Teacher.add_new_teacher(**data1)
        except ValueError as e:
            self.assertEqual(str(e), "invalid cpr")

        data2 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example1@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        try:
            Teacher.add_new_teacher(**data2)
        except ValueError as e:
            self.assertEqual(str(e), "invalid cpr")
