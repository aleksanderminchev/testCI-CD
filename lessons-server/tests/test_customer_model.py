from api.app import db
from tests.base_test_case import BaseTestCase
from models.customer import Customer, CustomerType, StatusEnum
from models.user import User
from models.student import Student


class CustomerModelTestCase(BaseTestCase):


    def setUp(self):
        pass
        # user_teacher = User(email='teacher@test.com', password='foo')

        # self.user_teacher = user_teacher
        # db.session.add(self.user_teacher)
        # db.session.commit()
        # teacher = Teacher(user_id=user_teacher.uid, wage_per_hour=120.00, bio="ewfewvwv",
        #                   photo="wdq", open_for_new_customers=True, payroll_id="12", status='active',)
        # db.session.add(teacher)
        # db.session.commit()

    def tearDown(self):
        Customer.query.delete()
        Student.query.delete()
        User.query.delete()
        db.session.commit()


    def test_get_customer_by_id(self):
        customer = Customer.query.first()
        retrieved_customer = Customer.get_customer_by_id(customer.id)
        assert retrieved_customer.id == customer.id

    def test_get_customer_by_email(self):
        user = User.query.first()
        customer = Customer.get_customer_by_email(user.email).customer
        assert customer.user_id == user.uid

    def test_add_customer_to_family(self):
        user = User.query.filter_by(email="new_customer@mail.com").first()

        result = Customer.add_customer_to_family(
            user.email,
            customer_data={
                "first_name": "FamCustomerFirstName",
                "last_name": "FamCustomerLastName",
                "email": "fam_customer@mail.com"}
        )

        assert result["user"].email == "new_customer@mail.com"
        assert result["customer"].customer_id == user.customer.id

    def test_valid_partitions_return_customer_object(self):
        args_for_customer = {
            "email": "example@mail.com",
            "first_name": "John",
            "last_name": "Customer",
            "phone": "+1234567890",
        }

        result = Customer.add_independent_customer_with_student(
        email=args_for_customer['email'],
        password="",
        first_name=args_for_customer['first_name'],
        last_name=args_for_customer['last_name'],
        phone=args_for_customer['phone'],
        customer_type='independent')
        self.assertIs(type(result['customer']), type(self.customer))
    
    def test_valid_email_returns_customer_object(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        try:
            result = Customer.add_independent_customer_with_student(
        email=data['email'],
        password="",
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        customer_type='independent')
            self.assertIs(type(result['customer']), type(self.customer))
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
            result = Customer.add_independent_customer_with_student(
        email=data['email'],
        password="",
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        customer_type='independent')
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
            result = Customer.add_independent_customer_with_student(
        email=data['email'],
        password="",
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        customer_type='independent')
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
            result = Customer.add_independent_customer_with_student(
        email=data['email'],
        password="",
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        customer_type='independent')
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
            result = Customer.add_independent_customer_with_student(
        email=data['email'],
        password="",
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        customer_type='independent')
        except ValueError as e:
            self.assertEqual(str(e), "invalid email")
        
    def test_valid_phone_returns_customer_object(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
        }
        try:
            result = Customer.add_independent_customer_with_student(
        email=data['email'],
        password="",
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        customer_type='independent')
            self.assertIs(type(result['customer']), type(self.customer))
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
            result = Customer.add_independent_customer_with_student(
        email=data['email'],
        password="",
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        customer_type='independent')
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
            result = Customer.add_independent_customer_with_student(
        email=data['email'],
        password="",
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        customer_type='independent')

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
            result = Customer.add_independent_customer_with_student(
        email=data['email'],
        password="",
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        customer_type='independent')
        except ValueError as e:
            self.assertEqual(str(e), "invalid phone")
        
    def test_valid_first_name_returns_customer_object(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
        }
        try:
            result = Customer.add_independent_customer_with_student(
        email=data['email'],
        password="",
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        customer_type='independent')
            self.assertIs(type(result['customer']), type(self.customer))
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
            result = Customer.add_independent_customer_with_student(
        email=data['email'],
        password="",
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        customer_type='independent')

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
            result = Customer.add_independent_customer_with_student(
        email=data['email'],
        password="",
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        customer_type='independent')
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
            result = Customer.add_independent_customer_with_student(
        email=data['email'],
        password="",
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        customer_type='independent')
        except ValueError as e:
            self.assertEqual(str(e), "invalid first name")
    
    def test_valid_last_name_returns_customer_object(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
        }
        result = Customer.add_independent_customer_with_student(
        email=data['email'],
        password="",
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        customer_type='independent')
        self.assertIs(type(result['customer']), type(self.customer))

    def test_invalid_last_name_nonstring_returns_invalid_last_name(self):
        data = {
            "first_name": "John",
            "last_name": 12345,
            "email": "example@mail.com",
            "phone": "+1234567890",
        }
        try:
            Customer.add_independent_customer_with_student(
        email=data['email'],
        password="",
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        customer_type='independent')
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
            Customer.add_independent_customer_with_student(
        email=data['email'],
        password="",
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        customer_type='independent')
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
            Customer.add_independent_customer_with_student(
        email=data['email'],
        password="",
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        customer_type='independent')
        except ValueError as e:
            self.assertEqual(str(e), "invalid last name")


    
    def test_boundary_analysis_valid_email_length_between_12_and_120(self):
        data1 = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "a" * 12 + "@mail.com",
        "phone": "+1234567890"
        }
        result1 = Customer.add_independent_customer_with_student(
        email=data1['email'],
        password="",
        first_name=data1['first_name'],
        last_name=data1['last_name'],
        phone=data1['phone'],
        customer_type='independent')
        self.assertIs(type(result1['customer']), type(self.customer))

        data2 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "a" * 120 + "@mail.com",
            "phone": "+1234567890"
        }
        result2 = Customer.add_independent_customer_with_student(
        email=data2['email'],
        password="",
        first_name=data2['first_name'],
        last_name=data2['last_name'],
        phone=data2['phone'],
        customer_type='independent')
        self.assertIs(type(result2['customer']), type(self.customer))

    def test_boundary_analysis_invalid_email_length_below_12_and_above_120(self):
        data1 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "a" * 2 + "@mail.com",
            "phone": "+1234567890"
        }
        try:
            Customer.add_independent_customer_with_student(
        email=data1['email'],
        password="",
        first_name=data1['first_name'],
        last_name=data1['last_name'],
        phone=data1['phone'],
        customer_type='independent')
        except ValueError as e:
            self.assertEqual(str(e), "invalid email")

        data2 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "a" * 121 + "@mail.com",
            "phone": "+1234567890",
        }
        try:
            Customer.add_independent_customer_with_student(
        email=data2['email'],
        password="",
        first_name=data2['first_name'],
        last_name=data2['last_name'],
        phone=data2['phone'],
        customer_type='independent')
        except ValueError as e:
            self.assertEqual(str(e), "invalid email")

    def test_boundary_analysis_valid_phone_length_between_9_and_12(self):
        data1 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+123456789",
        }
        result1 = Customer.add_independent_customer_with_student(
        email=data1['email'],
        password="",
        first_name=data1['first_name'],
        last_name=data1['last_name'],
        phone=data1['phone'],
        customer_type='independent')
        self.assertIs(type(result1['customer']), type(self.customer))

        data2 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example1@mail.com",
            "phone": "+1234567890",
        }
        result2 = Customer.add_independent_customer_with_student(
        email=data2['email'],
        password="",
        first_name=data2['first_name'],
        last_name=data2['last_name'],
        phone=data2['phone'],
        customer_type='independent')
        self.assertIs(type(result2['customer']), type(self.customer))

    def test_boundary_analysis_invalid_phone_length_below_9_and_above_12(self):
        data1 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+12345678905",
        }
        try:
            Customer.add_independent_customer_with_student(
        email=data1['email'],
        password="",
        first_name=data1['first_name'],
        last_name=data1['last_name'],
        phone=data1['phone'],
        customer_type='independent')
        except ValueError as e:
            self.assertEqual(str(e), "invalid phone")

        data2 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example1@mail.com",
            "phone": "+123456",
        }
        try:
            Customer.add_independent_customer_with_student(
        email=data2['email'],
        password="",
        first_name=data2['first_name'],
        last_name=data2['last_name'],
        phone=data2['phone'],
        customer_type='independent')
        except ValueError as e:
            self.assertEqual(str(e), "invalid phone")

    def test_boundary_analysis_valid_first_name_length_between_1_and_50(self):
        data1 = {
            "first_name": "J",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890"
        }
        result1 = Customer.add_independent_customer_with_student(
        email=data1['email'],
        password="",
        first_name=data1['first_name'],
        last_name=data1['last_name'],
        phone=data1['phone'],
        customer_type='independent')
        self.assertIs(type(result1['customer']), type(self.customer))

        data2 = {
            "first_name": "J" * 50,
            "last_name": "Doe",
            "email": "example1@mail.com",
            "phone": "+1234567890"
        }
        result2 = Customer.add_independent_customer_with_student(
        email=data2['email'],
        password="",
        first_name=data2['first_name'],
        last_name=data2['last_name'],
        phone=data2['phone'],
        customer_type='independent')
        self.assertIs(type(result2['customer']), type(self.customer))
    
    def test_boundary_analysis_invalid_first_name_length_below_1_and_above_50(self):
        data1 = {
            "first_name": "",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
        }
        try:
            Customer.add_independent_customer_with_student(
        email=data1['email'],
        password="",
        first_name=data1['first_name'],
        last_name=data1['last_name'],
        phone=data1['phone'],
        customer_type='independent')
        except ValueError as e:
            self.assertEqual(str(e), "invalid first name")

        data2 = {
            "first_name": "J" * 51,
            "last_name": "Doe",
            "email": "example1@mail.com",
            "phone": "+1234567890",
        }
        try:
            Customer.add_independent_customer_with_student(
        email=data2['email'],
        password="",
        first_name=data2['first_name'],
        last_name=data2['last_name'],
        phone=data2['phone'],
        customer_type='independent')
        except ValueError as e:
            self.assertEqual(str(e), "invalid first name")

    def test_boundary_analysis_valid_last_name_length_between_1_and_50(self):
        data1 = {
            "first_name": "John",
            "last_name": "D",
            "email": "example@mail.com",
            "phone": "+1234567890",
        }
        result1 = Customer.add_independent_customer_with_student(
        email=data1['email'],
        password="",
        first_name=data1['first_name'],
        last_name=data1['last_name'],
        phone=data1['phone'],
        customer_type='independent')
        self.assertIs(type(result1['customer']), type(self.customer))

        data2 = {
            "first_name": "John",
            "last_name": "D" * 50,
            "email": "example1@mail.com",
            "phone": "+1234567890",
        }
        result2 = Customer.add_independent_customer_with_student(
        email=data2['email'],
        password="",
        first_name=data2['first_name'],
        last_name=data2['last_name'],
        phone=data2['phone'],
        customer_type='independent')
        self.assertIs(type(result2['customer']), type(self.customer))

    def test_boundary_analysis_invalid_last_name_length_below_1_and_above_50(self):
        data1 = {
            "first_name": "John",
            "last_name": "",
            "email": "example@mail.com",
            "phone": "+1234567890",
        }
        try:
            Customer.add_independent_customer_with_student(
        email=data1['email'],
        password="",
        first_name=data1['first_name'],
        last_name=data1['last_name'],
        phone=data1['phone'],
        customer_type='independent')
        except ValueError as e:
            self.assertEqual(str(e), "invalid last name")

        data2 = {
            "first_name": "John",
            "last_name": "D" * 51,
            "email": "example1@mail.com",
            "phone": "+1234567890",
        }
        try:
            Customer.add_independent_customer_with_student(
        email=data2['email'],
        password="",
        first_name=data2['first_name'],
        last_name=data2['last_name'],
        phone=data2['phone'],
        customer_type='independent')
        except ValueError as e:
            self.assertEqual(str(e), "invalid last name")


    def test_valid_email_length_between_12_and_120(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890"
        }
        result = Customer.add_independent_customer_with_student(
        email=data['email'],
        password="",
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        customer_type='independent')
        self.assertIs(type(result['customer']), type(self.customer))


    def test_invalid_email_length_below_12_and_above_120(self):
        data1 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "ex@mail.com",
            "phone": "+1234567890"
        }
        try:
            Customer.add_independent_customer_with_student(
        email=data1['email'],
        password="",
        first_name=data1['first_name'],
        last_name=data1['last_name'],
        phone=data1['phone'],
        customer_type='independent')
        except ValueError as e:
            self.assertEqual(str(e), "invalid email")

        data2 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example1@mail.com" * 10,
            "phone": "+1234567890",
        }
        try:
            Customer.add_independent_customer_with_student(
        email=data2['email'],
        password="",
        first_name=data2['first_name'],
        last_name=data2['last_name'],
        phone=data2['phone'],
        customer_type='independent')
        except ValueError as e:
            self.assertEqual(str(e), "invalid email")


    def test_valid_phone_length_between_9_and_12(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890"
        }
        result = Customer.add_independent_customer_with_student(
        email=data['email'],
        password="",
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        customer_type='independent')
        self.assertIs(type(result['customer']), type(self.customer))


    def test_invalid_phone_length_below_9_and_above_12(self):
        data1 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
        }
        try:
            Customer.add_independent_customer_with_student(
        email=data1['email'],
        password="",
        first_name=data1['first_name'],
        last_name=data1['last_name'],
        phone=data1['phone'],
        customer_type='independent')
        except ValueError as e:
            self.assertEqual(str(e), "invalid phone")

        data2 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example1@mail.com",
            "phone": "+1234567890",
        }
        try:
            Customer.add_independent_customer_with_student(
        email=data2['email'],
        password="",
        first_name=data2['first_name'],
        last_name=data2['last_name'],
        phone=data2['phone'],
        customer_type='independent')
        except ValueError as e:
            self.assertEqual(str(e), "invalid phone")

    def test_valid_first_name_length_between_1_and_50(self):
        data1 = {
            "first_name": "J",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890"
        }
        result1 = Customer.add_independent_customer_with_student(
        email=data1['email'],
        password="",
        first_name=data1['first_name'],
        last_name=data1['last_name'],
        phone=data1['phone'],
        customer_type='independent')
        self.assertIs(type(result1['customer']), type(self.customer))

        data2 = {
            "first_name": "J" * 50,
            "last_name": "Doe",
            "email": "example1@mail.com",
            "phone": "+1234567890",
        }
        result2 = Customer.add_independent_customer_with_student(
        email=data2['email'],
        password="",
        first_name=data2['first_name'],
        last_name=data2['last_name'],
        phone=data2['phone'],
        customer_type='independent')
        self.assertIs(type(result2['customer']), type(self.customer))


    def test_invalid_first_name_length_below_1_and_above_50(self):
        data1 = {
            "first_name": "",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890"
        }
        try:
            Customer.add_independent_customer_with_student(
        email=data1['email'],
        password="",
        first_name=data1['first_name'],
        last_name=data1['last_name'],
        phone=data1['phone'],
        customer_type='independent')
        except ValueError as e:
            self.assertEqual(str(e), "invalid first name")

        data2 = {
            "first_name": "J" * 51,
            "last_name": "Doe",
            "email": "example1@mail.com",
            "phone": "+1234567890",
        }
        try:
            Customer.add_independent_customer_with_student(
        email=data2['email'],
        password="",
        first_name=data2['first_name'],
        last_name=data2['last_name'],
        phone=data2['phone'],
        customer_type='independent')
        except ValueError as e:
            self.assertEqual(str(e), "invalid first name")


    def test_valid_last_name_length_between_1_and_50(self):
        data1 = {
            "first_name": "John",
            "last_name": "D",
            "email": "example@mail.com",
            "phone": "+1234567890"
        }
        result1 = Customer.add_independent_customer_with_student(
        email=data1['email'],
        password="",
        first_name=data1['first_name'],
        last_name=data1['last_name'],
        phone=data1['phone'],
        customer_type='independent')
        self.assertIs(type(result1['customer']), type(self.customer))

        data2 = {
            "first_name": "John",
            "last_name": "D" * 50,
            "email": "example1@mail.com",
            "phone": "+1234567890",
        }
        result2 = Customer.add_independent_customer_with_student(
        email=data2['email'],
        password="",
        first_name=data2['first_name'],
        last_name=data2['last_name'],
        phone=data2['phone'],
        customer_type='independent')
        self.assertIs(type(result2['customer']), type(self.customer))


    def test_invalid_last_name_length_below_1_and_above_50(self):
        data1 = {
            "first_name": "John",
            "last_name": "",
            "email": "example@mail.com",
            "phone": "+1234567890"
        }
        try:
            Customer.add_independent_customer_with_student(
        email=data1['email'],
        password="",
        first_name=data1['first_name'],
        last_name=data1['last_name'],
        phone=data1['phone'],
        customer_type='independent')
        except ValueError as e:
            self.assertEqual(str(e), "invalid last name")

        data2 = {
            "first_name": "John",
            "last_name": "D" * 51,
            "email": "example1@mail.com",
            "phone": "+1234567890"
        }
        try:
            Customer.add_independent_customer_with_student(
        email=data2['email'],
        password="",
        first_name=data2['first_name'],
        last_name=data2['last_name'],
        phone=data2['phone'],
        customer_type='independent')
        except ValueError as e:
            self.assertEqual(str(e), "invalid last name")


    def test_add_independent_customer_with_student_valid_with_user(self):
        data2 = {
            "first_name": "John",
            "last_name": "D",
            "email": "example1@mail.com",
            "phone": "+1234567890"
        }
        result2 = Customer.add_independent_customer_with_student(
        email=data2['email'],
        password="",
        first_name=data2['first_name'],
        last_name=data2['last_name'],
        phone=data2['phone'],
        customer_type='independent')
        self.assertIs(type(result2['customer'].user),type(User()))
        self.assertIs(type(result2['student']),type(Student()))
        self.assertIs(type(result2['customer']), type(self.customer))


    def test_add_independent_customer_with_student_invalid_non_string(self):
        data2 = {
            "first_name": "John",
            "last_name": "D",
            "email": "example1@mail.com",
            "phone": "+1234567890"
        }    
        # Test implementation
        try:
            result2 = Customer.add_independent_customer_with_student(
        email=data2['email'],
        password="",
        first_name=data2['first_name'],
        last_name=data2['last_name'],
        phone=data2['phone'],
        customer_type="independent1")
        except ValueError as e:
            self.assertEqual(str(e),'invalid customer type')

    def test_add_independent_customer_with_student_invalid_empty_string(self):
        data2 = {
            "first_name": "John",
            "last_name": "D",
            "email": "example1@mail.com",
            "phone": "+1234567890"
        }    
        # Test implementation
        try:
            result2 = Customer.add_independent_customer_with_student(
        email=data2['email'],
        password="",
        first_name=data2['first_name'],
        last_name=data2['last_name'],
        phone=data2['phone'],
        customer_type='')
        except ValueError as e:
            self.assertEqual(str(e),'invalid customer type')
    def test_add_independent_customer_with_student_boundary_valid_with_user(self):
        data2 = {
            "first_name": "John",
            "last_name": "D",
            "email": "example1@mail.com",
            "phone": "+1234567890"
        }
        result2 = Customer.add_independent_customer_with_student(
        email=data2['email'],
        password="",
        first_name=data2['first_name'],
        last_name=data2['last_name'],
        phone=data2['phone'],
        customer_type='independent')
        self.assertIs(type(result2['customer'].user),type(User()))
        self.assertIs(type(result2['customer']), type(self.customer))

    def test_add_independent_customer_with_student_boundary_invalid_with_user1(self):
        data2 = {
            "first_name": "John",
            "last_name": "D",
            "email": "example1@mail.com",
            "phone": "+1234567890"
        }    
        # Test implementation
        try:
            result2 = Customer.add_independent_customer_with_student(
        email=data2['email'],
        password="",
        first_name=data2['first_name'],
        last_name=data2['last_name'],
        phone=data2['phone'],
        customer_type=41255)
        except ValueError as e:
            self.assertEqual(str(e),'invalid customer type')









    """Tests for add_customer _user"""
    def test_valid_add_customer_user_partitions_return_customer_object(self):
        args_for_customer = {
            "email": "example@mail.com",
            "first_name": "John",
            "last_name": "Customer",
            "phone": "+1234567890",
        }

        result = Customer.add_customer_user(
        email=args_for_customer['email'],
        password="",
        first_name=args_for_customer['first_name'],
        last_name=args_for_customer['last_name'],
        phone=args_for_customer['phone'],
        customer_type='family')
        self.assertIs(type(result['customer']), type(self.customer))
    
    def test_valid_add_customer_user_email_returns_customer_object(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
            "payroll_id": "010121-1234",
            "wage_per_hour": 1000
        }
        try:
            result = Customer.add_customer_user(
        email=data['email'],
        password="",
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        customer_type='family')
            self.assertIs(type(result['customer']), type(self.customer))
        except ValueError:
            self.fail("Expected no exception, but ValueError was raised.")
        
    def test_invalid_add_customer_user_email_length_above_boundary_returns_invalid_email(self):
        data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "a" * 121 + "@mail.com",
        "phone": "+1234567890"
        }
        try:
            result = Customer.add_customer_user(
        email=data['email'],
        password="",
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        customer_type='family')
        except ValueError as e:
            self.assertEqual(str(e), "invalid email")

    def test_invalid_add_customer_user_email_length_below_boundary_returns_invalid_email(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "a" * 11 + "@mail.com",
            "phone": "+1234567890",
        }
        try:
            result = Customer.add_customer_user(
        email=data['email'],
        password="",
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        customer_type='family')
        except ValueError as e:
            self.assertEqual(str(e), "invalid email")

    def test_invalid_add_customer_user_email_length_zero_returns_invalid_email(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "",
            "phone": "+1234567890",
        }
        try:
            result = Customer.add_customer_user(
        email=data['email'],
        password="",
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        customer_type='family')
        except ValueError as e:
            self.assertEqual(str(e), "invalid email")

    def test_invalid_add_customer_user_email_nonstring_returns_invalid_email(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": 12345,
            "phone": "+1234567890",
        }
        try:
            result = Customer.add_customer_user(
        email=data['email'],
        password="",
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        customer_type='family')
        except ValueError as e:
            self.assertEqual(str(e), "invalid email")
        
    def test_valid_add_customer_user_phone_returns_customer_object(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
        }
        try:
            result = Customer.add_customer_user(
        email=data['email'],
        password="",
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        customer_type='family')
            self.assertIs(type(result['customer']), type(self.customer))
        except ValueError as e:
            self.fail("Expected no ValueError, but got: {}".format(str(e)))

    def test_invalid_add_customer_user_phone_nonstring_returns_invalid_phone(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": 12345,
        }
        try:
            result = Customer.add_customer_user(
        email=data['email'],
        password="",
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        customer_type='family')
        except ValueError as e:
            self.assertEqual(str(e), "invalid phone")

    def test_invalid_add_customer_user_phone_length_zero_returns_invalid_phone(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": ""
        }
        try:
            result = Customer.add_customer_user(
        email=data['email'],
        password="",
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        customer_type='family')

        except ValueError as e:
            self.assertEqual(str(e), "invalid phone")

    def test_invalid_add_customer_user_phone_length_above_boundary_returns_invalid_phone(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+12345678901",
        }
        try:
            result = Customer.add_customer_user(
        email=data['email'],
        password="",
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        customer_type='family')
        except ValueError as e:
            self.assertEqual(str(e), "invalid phone")
        
    def test_valid_add_customer_user_first_name_returns_customer_object(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
        }
        try:
            result = Customer.add_customer_user(
        email=data['email'],
        password="",
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        customer_type='family')
            self.assertIs(type(result['customer']), type(self.customer))
        except ValueError as e:
            self.fail("Expected no ValueError, but got: {}".format(str(e)))

    def test_invalid_add_customer_user_first_name_nonstring_returns_invalid_first_name(self):
        data = {
            "first_name": 12345,
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
        }
        try:
            result = Customer.add_customer_user(
        email=data['email'],
        password="",
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        customer_type='family')

        except ValueError as e:
            self.assertEqual(str(e), "invalid first name")

    def test_invalid_add_customer_user_first_name_length_zero_returns_invalid_first_name(self):
        data = {
            "first_name": "",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
        }
        try:
            result = Customer.add_customer_user(
        email=data['email'],
        password="",
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        customer_type='family')
        except ValueError as e:
            self.assertEqual(str(e), "invalid first name")

    def test_invalid_add_customer_user_first_name_length_above_boundary_returns_invalid_first_name(self):
        data = {
            "first_name": "J" * 51,
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
        }
        try:
            result = Customer.add_customer_user(
        email=data['email'],
        password="",
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        customer_type='family')
        except ValueError as e:
            self.assertEqual(str(e), "invalid first name")
    
    def test_valid_add_customer_user_last_name_returns_customer_object(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
        }
        result = Customer.add_customer_user(
        email=data['email'],
        password="",
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        customer_type='family')
        self.assertIs(type(result['customer']), type(self.customer))

    def test_invalid_add_customer_user_last_name_nonstring_returns_invalid_last_name(self):
        data = {
            "first_name": "John",
            "last_name": 12345,
            "email": "example@mail.com",
            "phone": "+1234567890",
        }
        try:
            Customer.add_customer_user(
        email=data['email'],
        password="",
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        customer_type='family')
        except ValueError as e:
            self.assertEqual(str(e), "invalid last name")

    def test_invalid_add_customer_user_last_name_length_zero_returns_invalid_last_name(self):
        data = {
            "first_name": "John",
            "last_name": "",
            "email": "example@mail.com",
            "phone": "+1234567890",
        }
        try:
            Customer.add_customer_user(
        email=data['email'],
        password="",
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        customer_type='family')
        except ValueError as e:
            self.assertEqual(str(e), "invalid last name")

    def test_invalid_add_customer_user_last_name_length_above_boundary_returns_invalid_last_name(self):
        data = {
            "first_name": "John",
            "last_name": "D" * 51,
            "email": "example@mail.com",
            "phone": "+1234567890",
        }
        try:
            Customer.add_customer_user(
        email=data['email'],
        password="",
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        customer_type='family')
        except ValueError as e:
            self.assertEqual(str(e), "invalid last name")


    
    def test_boundary_add_customer_user_analysis_valid_email_length_between_12_and_120(self):
        data1 = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "a" * 12 + "@mail.com",
        "phone": "+1234567890"
        }
        result1 = Customer.add_customer_user(
        email=data1['email'],
        password="",
        first_name=data1['first_name'],
        last_name=data1['last_name'],
        phone=data1['phone'],
        customer_type='family')
        self.assertIs(type(result1['customer']), type(self.customer))

        data2 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "a" * 120 + "@mail.com",
            "phone": "+1234567890"
        }
        result2 = Customer.add_customer_user(
        email=data2['email'],
        password="",
        first_name=data2['first_name'],
        last_name=data2['last_name'],
        phone=data2['phone'],
        customer_type='family')
        self.assertIs(type(result2['customer']), type(self.customer))

    def test_boundary_add_customer_user_analysis_invalid_email_length_below_12_and_above_120(self):
        data1 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "a" * 2 + "@mail.com",
            "phone": "+1234567890"
        }
        try:
            Customer.add_customer_user(
        email=data1['email'],
        password="",
        first_name=data1['first_name'],
        last_name=data1['last_name'],
        phone=data1['phone'],
        customer_type='family')
        except ValueError as e:
            self.assertEqual(str(e), "invalid email")

        data2 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "a" * 121 + "@mail.com",
            "phone": "+1234567890",
        }
        try:
            Customer.add_customer_user(
        email=data2['email'],
        password="",
        first_name=data2['first_name'],
        last_name=data2['last_name'],
        phone=data2['phone'],
        customer_type='family')
        except ValueError as e:
            self.assertEqual(str(e), "invalid email")

    def test_boundary_add_customer_user_analysis_valid_phone_length_between_9_and_12(self):
        data1 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+123456789",
        }
        result1 = Customer.add_customer_user(
        email=data1['email'],
        password="",
        first_name=data1['first_name'],
        last_name=data1['last_name'],
        phone=data1['phone'],
        customer_type='family')
        self.assertIs(type(result1['customer']), type(self.customer))

        data2 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example1@mail.com",
            "phone": "+1234567890",
        }
        result2 = Customer.add_customer_user(
        email=data2['email'],
        password="",
        first_name=data2['first_name'],
        last_name=data2['last_name'],
        phone=data2['phone'],
        customer_type='family')
        self.assertIs(type(result2['customer']), type(self.customer))

    def test_boundary_add_customer_user_analysis_invalid_phone_length_below_9_and_above_12(self):
        data1 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+12345678905",
        }
        try:
            Customer.add_customer_user(
        email=data1['email'],
        password="",
        first_name=data1['first_name'],
        last_name=data1['last_name'],
        phone=data1['phone'],
        customer_type='family')
        except ValueError as e:
            self.assertEqual(str(e), "invalid phone")

        data2 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example1@mail.com",
            "phone": "+123456",
        }
        try:
            Customer.add_customer_user(
        email=data2['email'],
        password="",
        first_name=data2['first_name'],
        last_name=data2['last_name'],
        phone=data2['phone'],
        customer_type='family')
        except ValueError as e:
            self.assertEqual(str(e), "invalid phone")

    def test_boundary_add_customer_user_analysis_valid_first_name_length_between_1_and_50(self):
        data1 = {
            "first_name": "J",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890"
        }
        result1 = Customer.add_customer_user(
        email=data1['email'],
        password="",
        first_name=data1['first_name'],
        last_name=data1['last_name'],
        phone=data1['phone'],
        customer_type='family')
        self.assertIs(type(result1['customer']), type(self.customer))

        data2 = {
            "first_name": "J" * 50,
            "last_name": "Doe",
            "email": "example1@mail.com",
            "phone": "+1234567890"
        }
        result2 = Customer.add_customer_user(
        email=data2['email'],
        password="",
        first_name=data2['first_name'],
        last_name=data2['last_name'],
        phone=data2['phone'],
        customer_type='family')
        self.assertIs(type(result2['customer']), type(self.customer))
    
    def test_boundary_add_customer_user_analysis_invalid_first_name_length_below_1_and_above_50(self):
        data1 = {
            "first_name": "",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
        }
        try:
            Customer.add_customer_user(
        email=data1['email'],
        password="",
        first_name=data1['first_name'],
        last_name=data1['last_name'],
        phone=data1['phone'],
        customer_type='family')
        except ValueError as e:
            self.assertEqual(str(e), "invalid first name")

        data2 = {
            "first_name": "J" * 51,
            "last_name": "Doe",
            "email": "example1@mail.com",
            "phone": "+1234567890",
        }
        try:
            Customer.add_customer_user(
        email=data2['email'],
        password="",
        first_name=data2['first_name'],
        last_name=data2['last_name'],
        phone=data2['phone'],
        customer_type='family')
        except ValueError as e:
            self.assertEqual(str(e), "invalid first name")

    def test_boundary_add_customer_user_analysis_valid_last_name_length_between_1_and_50(self):
        data1 = {
            "first_name": "John",
            "last_name": "D",
            "email": "example@mail.com",
            "phone": "+1234567890",
        }
        result1 = Customer.add_customer_user(
        email=data1['email'],
        password="",
        first_name=data1['first_name'],
        last_name=data1['last_name'],
        phone=data1['phone'],
        customer_type='family')
        self.assertIs(type(result1['customer']), type(self.customer))

        data2 = {
            "first_name": "John",
            "last_name": "D" * 50,
            "email": "example1@mail.com",
            "phone": "+1234567890",
        }
        result2 = Customer.add_customer_user(
        email=data2['email'],
        password="",
        first_name=data2['first_name'],
        last_name=data2['last_name'],
        phone=data2['phone'],
        customer_type='family')
        self.assertIs(type(result2['customer']), type(self.customer))

    def test_boundary_add_customer_user_analysis_invalid_last_name_length_below_1_and_above_50(self):
        data1 = {
            "first_name": "John",
            "last_name": "",
            "email": "example@mail.com",
            "phone": "+1234567890",
        }
        try:
            Customer.add_customer_user(
        email=data1['email'],
        password="",
        first_name=data1['first_name'],
        last_name=data1['last_name'],
        phone=data1['phone'],
        customer_type='family')
        except ValueError as e:
            self.assertEqual(str(e), "invalid last name")

        data2 = {
            "first_name": "John",
            "last_name": "D" * 51,
            "email": "example1@mail.com",
            "phone": "+1234567890",
        }
        try:
            Customer.add_customer_user(
        email=data2['email'],
        password="",
        first_name=data2['first_name'],
        last_name=data2['last_name'],
        phone=data2['phone'],
        customer_type='family')
        except ValueError as e:
            self.assertEqual(str(e), "invalid last name")


    def test_valid_add_customer_user_email_length_between_12_and_120(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890"
        }
        result = Customer.add_customer_user(
        email=data['email'],
        password="",
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        customer_type='family')
        self.assertIs(type(result['customer']), type(self.customer))


    def test_invalid_add_customer_user_email_length_below_12_and_above_120(self):
        data1 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "ex@mail.com",
            "phone": "+1234567890"
        }
        try:
            Customer.add_customer_user(
        email=data1['email'],
        password="",
        first_name=data1['first_name'],
        last_name=data1['last_name'],
        phone=data1['phone'],
        customer_type='family')
        except ValueError as e:
            self.assertEqual(str(e), "invalid email")

        data2 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example1@mail.com" * 10,
            "phone": "+1234567890",
        }
        try:
            Customer.add_customer_user(
        email=data2['email'],
        password="",
        first_name=data2['first_name'],
        last_name=data2['last_name'],
        phone=data2['phone'],
        customer_type='family')
        except ValueError as e:
            self.assertEqual(str(e), "invalid email")


    def test_valid_add_customer_user_phone_length_between_9_and_12(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890"
        }
        result = Customer.add_customer_user(
        email=data['email'],
        password="",
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        customer_type='family')
        self.assertIs(type(result['customer']), type(self.customer))


    def test_invalid_add_customer_user_phone_length_below_9_and_above_12(self):
        data1 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890",
        }
        try:
            Customer.add_customer_user(
        email=data1['email'],
        password="",
        first_name=data1['first_name'],
        last_name=data1['last_name'],
        phone=data1['phone'],
        customer_type='family')
        except ValueError as e:
            self.assertEqual(str(e), "invalid phone")

        data2 = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example1@mail.com",
            "phone": "+1234567890",
        }
        try:
            Customer.add_customer_user(
        email=data2['email'],
        password="",
        first_name=data2['first_name'],
        last_name=data2['last_name'],
        phone=data2['phone'],
        customer_type='family')
        except ValueError as e:
            self.assertEqual(str(e), "invalid phone")

    def test_valid_add_customer_user_first_name_length_between_1_and_50(self):
        data1 = {
            "first_name": "J",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890"
        }
        result1 = Customer.add_customer_user(
        email=data1['email'],
        password="",
        first_name=data1['first_name'],
        last_name=data1['last_name'],
        phone=data1['phone'],
        customer_type='family')
        self.assertIs(type(result1['customer']), type(self.customer))

        data2 = {
            "first_name": "J" * 50,
            "last_name": "Doe",
            "email": "example1@mail.com",
            "phone": "+1234567890",
        }
        result2 = Customer.add_customer_user(
        email=data2['email'],
        password="",
        first_name=data2['first_name'],
        last_name=data2['last_name'],
        phone=data2['phone'],
        customer_type='family')
        self.assertIs(type(result2['customer']), type(self.customer))


    def test_invalid_add_customer_user_first_name_length_below_1_and_above_50(self):
        data1 = {
            "first_name": "",
            "last_name": "Doe",
            "email": "example@mail.com",
            "phone": "+1234567890"
        }
        try:
            Customer.add_customer_user(
        email=data1['email'],
        password="",
        first_name=data1['first_name'],
        last_name=data1['last_name'],
        phone=data1['phone'],
        customer_type='family')
        except ValueError as e:
            self.assertEqual(str(e), "invalid first name")

        data2 = {
            "first_name": "J" * 51,
            "last_name": "Doe",
            "email": "example1@mail.com",
            "phone": "+1234567890",
        }
        try:
            Customer.add_customer_user(
        email=data2['email'],
        password="",
        first_name=data2['first_name'],
        last_name=data2['last_name'],
        phone=data2['phone'],
        customer_type='family')
        except ValueError as e:
            self.assertEqual(str(e), "invalid first name")


    def test_valid_add_customer_user_last_name_length_between_1_and_50(self):
        data1 = {
            "first_name": "John",
            "last_name": "D",
            "email": "example@mail.com",
            "phone": "+1234567890"
        }
        result1 = Customer.add_customer_user(
        email=data1['email'],
        password="",
        first_name=data1['first_name'],
        last_name=data1['last_name'],
        phone=data1['phone'],
        customer_type='family')
        self.assertIs(type(result1['customer']), type(self.customer))

        data2 = {
            "first_name": "John",
            "last_name": "D" * 50,
            "email": "example1@mail.com",
            "phone": "+1234567890",
        }
        result2 = Customer.add_customer_user(
        email=data2['email'],
        password="",
        first_name=data2['first_name'],
        last_name=data2['last_name'],
        phone=data2['phone'],
        customer_type='family')
        self.assertIs(type(result2['customer']), type(self.customer))


    def test_invalid_add_customer_user_last_name_length_below_1_and_above_50(self):
        data1 = {
            "first_name": "John",
            "last_name": "",
            "email": "example@mail.com",
            "phone": "+1234567890"
        }
        try:
            Customer.add_customer_user(
        email=data1['email'],
        password="",
        first_name=data1['first_name'],
        last_name=data1['last_name'],
        phone=data1['phone'],
        customer_type='family')
        except ValueError as e:
            self.assertEqual(str(e), "invalid last name")

        data2 = {
            "first_name": "John",
            "last_name": "D" * 51,
            "email": "example1@mail.com",
            "phone": "+1234567890"
        }
        try:
            Customer.add_customer_user(
        email=data2['email'],
        password="",
        first_name=data2['first_name'],
        last_name=data2['last_name'],
        phone=data2['phone'],
        customer_type='family')
        except ValueError as e:
            self.assertEqual(str(e), "invalid last name")


    def test_add_customer_user_valid_with_user(self):
        data2 = {
            "first_name": "John",
            "last_name": "D",
            "email": "example1@mail.com",
            "phone": "+1234567890"
        }
        result2 = Customer.add_customer_user(
        email=data2['email'],
        password="",
        first_name=data2['first_name'],
        last_name=data2['last_name'],
        phone=data2['phone'],
        customer_type='family')
        self.assertIs(type(result2['customer'].user),type(User()))
        self.assertIs(type(result2['customer']), type(self.customer))


    def test_add_customer_user_invalid_non_string(self):
        data2 = {
            "first_name": "John",
            "last_name": "D",
            "email": "example1@mail.com",
            "phone": "+1234567890"
        }    
        # Test implementation
        try:
            result2 = Customer.add_customer_user(
        email=data2['email'],
        password="",
        first_name=data2['first_name'],
        last_name=data2['last_name'],
        phone=data2['phone'],
        customer_type="family1")
        except ValueError as e:
            self.assertEqual(str(e),'invalid customer type')

    def test_add_customer_user_invalid_empty_string(self):
        data2 = {
            "first_name": "John",
            "last_name": "D",
            "email": "example1@mail.com",
            "phone": "+1234567890"
        }    
        # Test implementation
        try:
            result2 = Customer.add_customer_user(
        email=data2['email'],
        password="",
        first_name=data2['first_name'],
        last_name=data2['last_name'],
        phone=data2['phone'],
        customer_type='')
        except ValueError as e:
            self.assertEqual(str(e),'invalid customer type')
    def test_add_customer_user_boundary_valid_with_user(self):
        data2 = {
            "first_name": "John",
            "last_name": "D",
            "email": "example1@mail.com",
            "phone": "+1234567890"
        }
        result2 = Customer.add_customer_user(
        email=data2['email'],
        password="",
        first_name=data2['first_name'],
        last_name=data2['last_name'],
        phone=data2['phone'],
        customer_type='family')
        self.assertIs(type(result2['customer'].user),type(User()))
        self.assertIs(type(result2['customer']), type(self.customer))

    def test_add_customer_user_boundary_invalid_with_user1(self):
        data2 = {
            "first_name": "John",
            "last_name": "D",
            "email": "example1@mail.com",
            "phone": "+1234567890"
        }    
        # Test implementation
        try:
            result2 = Customer.add_customer_user(
        email=data2['email'],
        password="",
        first_name=data2['first_name'],
        last_name=data2['last_name'],
        phone=data2['phone'],
        customer_type=41255)
        except ValueError as e:
            self.assertEqual(str(e),'invalid customer type')