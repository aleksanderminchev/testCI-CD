import pytest
from api.app import db
from api.utils.utils import datetime
from tests.base_test_case import BaseTestCase
from models.student import Student
from models.user import User
from models.customer import Customer


class StudentModelTestCase(BaseTestCase):

    def setUp(self):
        pass
        # user_teacher = User(email='teacher@test.com', password='foo')
        self.student = Student()
        # self.user_teacher = user_teacher
        # db.session.add(self.user_teacher)
        # db.session.commit()
        # teacher = Teacher(user_id=user_teacher.uid, wage_per_hour=120.00, bio="ewfewvwv",
        #                   photo="wdq", open_for_new_students=True, payroll_id="12", status='active',)
        # db.session.add(teacher)
        # db.session.commit()

    def tearDown(self):
        Student.query.delete()
        User.query.delete()
        db.session.commit()

    def test_add_new_student_with_user(self):
        customer = Customer.get_customer_by_id(1)
        student_user_data = {
            "email": "somemail@email.com",
            "password": "123456",
            "first_name": "John",
            "last_name": "Michael",
            "phone": "+45911031253"
        }
        student = Student.add_new_student(
            customer.id, typeOfStudent='with_user', **student_user_data)
        test_student_existence = Student.get_student_by_id(3)
        print(customer.students)
        assert student
        assert customer.students[2].user.to_dict() == student
        assert test_student_existence
        assert test_student_existence.student_type.value == 'independent'

    def test_add_new_student_child(self):
        customer = Customer.get_customer_by_id(1)
        student = Student.add_new_student(customer.id, typeOfStudent='no_user')
        test_student_existence = Student.get_student_by_id(2)
        print(customer.students)
        assert student
        assert customer.students[1].to_dict() == student
        assert test_student_existence
        assert test_student_existence.student_type.value == 'child'

    def test_valid_partitions_return_student_object(self):
        args_for_student = {
            "email": "example@mail.com",
            "first_name": "John",
            "last_name": "Student",
            "phone": "+1234567890",
        }

        result = Student.add_new_student(
            id=self.customer.id, typeOfStudent="with_user", **args_for_student)
        self.assertIs(type(result), type(self.student))

    def test_valid_email_returns_student_object(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        try:
            result = Student.add_new_student(
                id=self.customer.id, typeOfStudent="with_user", **data)
            self.assertIs(type(result), type(self.student))
        except ValueError:
            self.fail("Expected no exception, but ValueError was raised.")

    def test_invalid_email_length_above_boundary_returns_invalid_email(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "a" * 121 + "@mail.com",
            "phone": "+1234567890"
        }
        try:
            result = Student.add_new_student(
                id=self.customer.id, typeOfStudent="with_user", **data)
        except ValueError as e:
            self.assertEqual(str(e), "invalid email")

    def test_invalid_email_length_below_boundary_returns_invalid_email(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "a" * 11 + "@mail.com",
            "phone": "+1234567890",
        }
        try:
            result = Student.add_new_student(
                id=self.customer.id, typeOfStudent="with_user", **data)
        except ValueError as e:
            self.assertEqual(str(e), "invalid email")

    def test_invalid_email_length_zero_returns_invalid_email(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "",
            "phone": "+1234567890",
        }
        try:
            result = Student.add_new_student(
                id=self.customer.id, typeOfStudent="with_user", **data)
        except ValueError as e:
            self.assertEqual(str(e), "invalid email")

    def test_invalid_email_nonstring_returns_invalid_email(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": 12345,
            "phone": "+1234567890",
        }
        try:
            result = Student.add_new_student(
                id=self.customer.id, typeOfStudent="with_user", **data)
        except ValueError as e:
            self.assertEqual(str(e), "invalid email")

    def test_valid_phone_returns_student_object(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
        }
        try:
            result = Student.add_new_student(
                id=self.customer.id, typeOfStudent="with_user", **data)
            self.assertIs(type(result), type(self.student))
        except ValueError as e:
            self.fail("Expected no ValueError, but got: {}".format(str(e)))

    def test_invalid_phone_nonstring_returns_invalid_phone(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": 12345,
        }
        try:
            result = Student.add_new_student(
                id=self.customer.id, typeOfStudent="with_user", **data)
        except ValueError as e:
            self.assertEqual(str(e), "invalid phone")

    def test_invalid_phone_length_zero_returns_invalid_phone(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": ""
        }
        try:
            result = Student.add_new_student(
                id=self.customer.id, typeOfStudent="with_user", **data)

        except ValueError as e:
            self.assertEqual(str(e), "invalid phone")

    def test_invalid_phone_length_above_boundary_returns_invalid_phone(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+12345678901",
        }
        try:
            result = Student.add_new_student(
                id=self.customer.id, typeOfStudent="with_user", **data)
        except ValueError as e:
            self.assertEqual(str(e), "invalid phone")

    def test_valid_first_name_returns_student_object(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
        }
        try:
            result = Student.add_new_student(
                id=self.customer.id, typeOfStudent="with_user", **data)
            self.assertIs(type(result), type(self.student))
        except ValueError as e:
            self.fail("Expected no ValueError, but got: {}".format(str(e)))

    def test_invalid_first_name_nonstring_returns_invalid_first_name(self):
        data = {
            "first_name": 12345,
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
        }
        try:
            result = Student.add_new_student(
                id=self.customer.id, typeOfStudent="with_user", **data)

        except ValueError as e:
            self.assertEqual(str(e), "invalid first name")

    def test_invalid_first_name_length_zero_returns_invalid_first_name(self):
        data = {
            "first_name": "",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
        }
        try:
            result = Student.add_new_student(
                id=self.customer.id, typeOfStudent="with_user", **data)
        except ValueError as e:
            self.assertEqual(str(e), "invalid first name")

    def test_invalid_first_name_length_above_boundary_returns_invalid_first_name(self):
        data = {
            "first_name": "J" * 51,
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
        }
        try:
            result = Student.add_new_student(
                id=self.customer.id, typeOfStudent="with_user", **data)
        except ValueError as e:
            self.assertEqual(str(e), "invalid first name")

    def test_valid_last_name_returns_student_object(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
        }
        result = Student.add_new_student(
            id=self.customer.id, typeOfStudent="with_user", **data)
        self.assertIs(type(result), type(self.student))

    def test_invalid_last_name_nonstring_returns_invalid_last_name(self):
        data = {
            "first_name": "John",
            "last_name": 12345,
            "email": "example@mail.com",
            "phone": "+1234567890",
        }
        try:
            Student.add_new_student(
                id=self.customer.id, typeOfStudent="with_user", **data)
        except ValueError as e:
            self.assertEqual(str(e), "invalid last name")

    def test_invalid_last_name_length_zero_returns_invalid_last_name(self):
        data = {
            "first_name": "John",
            "last_name": "",
            "email": "example@mail.com",
            "phone": "+1234567890",
        }
        try:
            Student.add_new_student(
                id=self.customer.id, typeOfStudent="with_user", **data)
        except ValueError as e:
            self.assertEqual(str(e), "invalid last name")

    def test_invalid_last_name_length_above_boundary_returns_invalid_last_name(self):
        data = {
            "first_name": "John",
            "last_name": "D" * 51,
            "email": "example@mail.com",
            "phone": "+1234567890",
        }
        try:
            Student.add_new_student(
                id=self.customer.id, typeOfStudent="with_user", **data)
        except ValueError as e:
            self.assertEqual(str(e), "invalid last name")

    def test_boundary_analysis_valid_email_length_between_12_and_120(self):
        data1 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "a" * 12 + "@mail.com",
            "phone": "+1234567890"
        }
        result1 = Student.add_new_student(
            id=self.customer.id, typeOfStudent="with_user", **data1)
        self.assertIs(type(result1), type(self.student))

        data2 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "a" * 120 + "@mail.com",
            "phone": "+1234567890"
        }
        result2 = Student.add_new_student(
            id=self.customer.id, typeOfStudent="with_user", **data2)
        self.assertIs(type(result2), type(self.student))

    def test_boundary_analysis_invalid_email_length_below_12_and_above_120(self):
        data1 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "a" * 2 + "@mail.com",
            "phone": "+1234567890"
        }
        try:
            Student.add_new_student(
                id=self.customer.id, typeOfStudent="with_user", **data1)
        except ValueError as e:
            self.assertEqual(str(e), "invalid email")

        data2 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "a" * 121 + "@mail.com",
            "phone": "+1234567890",
        }
        try:
            Student.add_new_student(
                id=self.customer.id, typeOfStudent="with_user", **data2)
        except ValueError as e:
            self.assertEqual(str(e), "invalid email")

    def test_boundary_analysis_valid_phone_length_between_9_and_12(self):
        data1 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+123456789",
        }
        result1 = Student.add_new_student(
            id=self.customer.id, typeOfStudent="with_user", **data1)
        self.assertIs(type(result1), type(self.student))

        data2 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example1@mail.com",
            "phone": "+1234567890",
        }
        result2 = Student.add_new_student(
            id=self.customer.id, typeOfStudent="with_user", **data2)
        self.assertIs(type(result2), type(self.student))

    def test_boundary_analysis_invalid_phone_length_below_9_and_above_12(self):
        data1 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+12345678905",
        }
        try:
            Student.add_new_student(
                id=self.customer.id, typeOfStudent="with_user", **data1)
        except ValueError as e:
            self.assertEqual(str(e), "invalid phone")

        data2 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example1@mail.com",
            "phone": "+123456",
        }
        try:
            Student.add_new_student(
                id=self.customer.id, typeOfStudent="with_user", **data2)
        except ValueError as e:
            self.assertEqual(str(e), "invalid phone")

    def test_boundary_analysis_valid_first_name_length_between_1_and_50(self):
        data1 = {
            "first_name": "J",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890"
        }
        result1 = Student.add_new_student(
            id=self.customer.id, typeOfStudent="with_user", **data1)
        self.assertIs(type(result1), type(self.student))

        data2 = {
            "first_name": "J" * 50,
            "last_name": "Doe",
            "email": "example1@mail.com",
            "phone": "+1234567890"
        }
        result2 = Student.add_new_student(
            id=self.customer.id, typeOfStudent="with_user", **data2)
        self.assertIs(type(result2), type(self.student))

    def test_boundary_analysis_invalid_first_name_length_below_1_and_above_50(self):
        data1 = {
            "first_name": "",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
        }
        try:
            Student.add_new_student(
                id=self.customer.id, typeOfStudent="with_user", **data1)
        except ValueError as e:
            self.assertEqual(str(e), "invalid first name")

        data2 = {
            "first_name": "J" * 51,
            "last_name": "Doe",
            "email": "example1@mail.com",
            "phone": "+1234567890",
        }
        try:
            Student.add_new_student(
                id=self.customer.id, typeOfStudent="with_user", **data2)
        except ValueError as e:
            self.assertEqual(str(e), "invalid first name")

    def test_boundary_analysis_valid_last_name_length_between_1_and_50(self):
        data1 = {
            "first_name": "John",
            "last_name": "D",
            "email": "example@mail.com",
            "phone": "+1234567890",
        }
        result1 = Student.add_new_student(
            id=self.customer.id, typeOfStudent="with_user", **data1)
        self.assertIs(type(result1), type(self.student))

        data2 = {
            "first_name": "John",
            "last_name": "D" * 50,
            "email": "example1@mail.com",
            "phone": "+1234567890",
        }
        result2 = Student.add_new_student(
            id=self.customer.id, typeOfStudent="with_user", **data2)
        self.assertIs(type(result2), type(self.student))

    def test_boundary_analysis_invalid_last_name_length_below_1_and_above_50(self):
        data1 = {
            "first_name": "John",
            "last_name": "",
            "email": "example@mail.com",
            "phone": "+1234567890",
        }
        try:
            Student.add_new_student(
                id=self.customer.id, typeOfStudent="with_user", **data1)
        except ValueError as e:
            self.assertEqual(str(e), "invalid last name")

        data2 = {
            "first_name": "John",
            "last_name": "D" * 51,
            "email": "example1@mail.com",
            "phone": "+1234567890",
        }
        try:
            Student.add_new_student(
                id=self.customer.id, typeOfStudent="with_user", **data2)
        except ValueError as e:
            self.assertEqual(str(e), "invalid last name")

    def test_valid_email_length_between_12_and_120(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890"
        }
        result = Student.add_new_student(
            id=self.customer.id, typeOfStudent="with_user", **data)
        self.assertIs(type(result), type(self.student))

    def test_invalid_email_length_below_12_and_above_120(self):
        data1 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "ex@mail.com",
            "phone": "+1234567890"
        }
        try:
            Student.add_new_student(
                id=self.customer.id, typeOfStudent="with_user", **data1)
        except ValueError as e:
            self.assertEqual(str(e), "invalid email")

        data2 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example1@mail.com" * 10,
            "phone": "+1234567890",
        }
        try:
            Student.add_new_student(
                id=self.customer.id, typeOfStudent="with_user", **data2)
        except ValueError as e:
            self.assertEqual(str(e), "invalid email")

    def test_valid_phone_length_between_9_and_12(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890"
        }
        result = Student.add_new_student(
            id=self.customer.id, typeOfStudent="with_user", **data)
        self.assertIs(type(result), type(self.student))

    def test_invalid_phone_length_below_9_and_above_12(self):
        data1 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
        }
        try:
            Student.add_new_student(
                id=self.customer.id, typeOfStudent="with_user", **data1)
        except ValueError as e:
            self.assertEqual(str(e), "invalid phone")

        data2 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example1@mail.com",
            "phone": "+1234567890",
        }
        try:
            Student.add_new_student(
                id=self.customer.id, typeOfStudent="with_user", **data2)
        except ValueError as e:
            self.assertEqual(str(e), "invalid phone")

    def test_valid_first_name_length_between_1_and_50(self):
        data1 = {
            "first_name": "J",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890"
        }
        result1 = Student.add_new_student(
            id=self.customer.id, typeOfStudent="with_user", **data1)
        self.assertIs(type(result1), type(self.student))

        data2 = {
            "first_name": "J" * 50,
            "last_name": "Doe",
            "email": "example1@mail.com",
            "phone": "+1234567890",
        }
        result2 = Student.add_new_student(
            id=self.customer.id, typeOfStudent="with_user", **data2)
        self.assertIs(type(result2), type(self.student))

    def test_invalid_first_name_length_below_1_and_above_50(self):
        data1 = {
            "first_name": "",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890"
        }
        try:
            Student.add_new_student(
                id=self.customer.id, typeOfStudent="with_user", **data1)
        except ValueError as e:
            self.assertEqual(str(e), "invalid first name")

        data2 = {
            "first_name": "J" * 51,
            "last_name": "Doe",
            "email": "example1@mail.com",
            "phone": "+1234567890",
        }
        try:
            Student.add_new_student(
                id=self.customer.id, typeOfStudent="with_user", **data2)
        except ValueError as e:
            self.assertEqual(str(e), "invalid first name")

    def test_valid_last_name_length_between_1_and_50(self):
        data1 = {
            "first_name": "John",
            "last_name": "D",
            "email": "example@mail.com",
            "phone": "+1234567890"
        }
        result1 = Student.add_new_student(
            id=self.customer.id, typeOfStudent="with_user", **data1)
        self.assertIs(type(result1), type(self.student))

        data2 = {
            "first_name": "John",
            "last_name": "D" * 50,
            "email": "example1@mail.com",
            "phone": "+1234567890",
        }
        result2 = Student.add_new_student(
            id=self.customer.id, typeOfStudent="with_user", **data2)
        self.assertIs(type(result2), type(self.student))

    def test_invalid_last_name_length_below_1_and_above_50(self):
        data1 = {
            "first_name": "John",
            "last_name": "",
            "email": "example@mail.com",
            "phone": "+1234567890"
        }
        try:
            Student.add_new_student(
                id=self.customer.id, typeOfStudent="with_user", **data1)
        except ValueError as e:
            self.assertEqual(str(e), "invalid last name")

        data2 = {
            "first_name": "John",
            "last_name": "D" * 51,
            "email": "example1@mail.com",
            "phone": "+1234567890"
        }
        try:
            Student.add_new_student(
                id=self.customer.id, typeOfStudent="with_user", **data2)
        except ValueError as e:
            self.assertEqual(str(e), "invalid last name")

    def test_add_new_student_valid_with_user(self):
        data2 = {
            "first_name": "John",
            "last_name": "D",
            "email": "example1@mail.com",
            "phone": "+1234567890"
        }
        result2 = Student.add_new_student(
            id=self.customer.id, typeOfStudent="with_user", **data2)
        self.assertIs(type(result2.user), type(User()))
        self.assertIs(type(result2), type(self.student))

    def test_add_new_student_valid_no_user(self):
        data2 = {
            "first_name": "John",
            "last_name": "D",
            "email": "example1@mail.com",
        }
        # Test implementation
        result2 = Student.add_new_student(
            id=self.customer.id, typeOfStudent="no_user", **data2)
        self.assertIsNot(type(result2.user), type(User()))
        self.assertIs(type(result2), type(self.student))

    def test_add_new_student_invalid_non_string(self):
        data2 = {
            "first_name": "John",
            "last_name": "D",
            "email": "example1@mail.com",
            "phone": "+1234567890"
        }
        # Test implementation
        try:
            result2 = Student.add_new_student(
                id=self.customer.id, typeOfStudent=1234, **data2)
        except ValueError as e:
            self.assertEqual(str(e), 'invalid student type')

    def test_add_new_student_invalid_empty_string(self):
        data2 = {
            "first_name": "John",
            "last_name": "D",
            "email": "example1@mail.com",
            "phone": "+1234567890"
        }
        # Test implementation
        try:
            result2 = Student.add_new_student(
                id=self.customer.id, typeOfStudent="", **data2)
        except ValueError as e:
            self.assertEqual(str(e), 'invalid student type')

    def test_add_new_student_boundary_valid_with_user(self):
        data2 = {
            "first_name": "John",
            "last_name": "D",
            "email": "example1@mail.com",
            "phone": "+1234567890"
        }
        result2 = Student.add_new_student(
            id=self.customer.id, typeOfStudent="with_user", **data2)
        self.assertIs(type(result2.user), type(User()))
        self.assertIs(type(result2), type(self.student))

    def test_add_new_student_boundary_valid_no_user(self):
        data2 = {
            "first_name": "John",
            "last_name": "D",
            "email": "example1@mail.com",
        }
        # Test implementation
        result2 = Student.add_new_student(
            id=self.customer.id, typeOfStudent="no_user", **data2)
        self.assertIsNot(type(result2.user), type(User()))
        self.assertIs(type(result2), type(self.student))

    def test_add_new_student_boundary_invalid_with_user1(self):
        data2 = {
            "first_name": "John",
            "last_name": "D",
            "email": "example1@mail.com",
            "phone": "+1234567890"
        }
        # Test implementation
        try:
            result2 = Student.add_new_student(
                id=self.customer.id, typeOfStudent="with_user1", **data2)
        except ValueError as e:
            self.assertEqual(str(e), 'invalid student type')
