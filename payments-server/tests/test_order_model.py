from api.app import db
from tests.base_test_case import BaseTestCase
from models.order import Order, OrderStatus
from models.customer import Customer
from unittest.mock import Mock

class OrderModelTestCase(BaseTestCase):

    

    def setUp(self):
        # user_teacher = User(email='teacher@test.com', password='foo')
        self.student=Order()
        mock_data=Mock()
        mock_data.crm_deal_id = ""
        mock_data.stripe_customer_id = ""
        mock_data.extra_student = 0
        mock_data.discount = None
        mock_data.upsell = False
        self.mock_data = mock_data
        # self.user_teacher = user_teacher
        # db.session.add(self.user_teacher)
        # db.session.commit()
        # teacher = Teacher(user_id=user_teacher.uid, wage_per_hour=120.00, bio="ewfewvwv",
        #                   photo="wdq", open_for_new_students=True, payroll_id="12", status='active',)
        # db.session.add(teacher)
        # db.session.commit()

    def tearDown(self):
        Order.query.delete()
        db.session.commit()
    # def test_create_and_update_order(self):
    #     kwargs = {
    #         'customer_type': 'family',
    #         'stripe_id': '31',
    #     }

    #     customer_user = Customer.add_customer_user(
    #         'customerOrder@mail.com', '123', 'John', 'Doe', '312213', **kwargs)

    #     assert customer_user
    #     assert customer_user['customer']
    #     assert customer_user['user']
    #     assert customer_user['customer'].customer_type.value == 'family'
    #     assert customer_user['customer'].stripe_id == '31'

    #     order_data = {
    #         'total_hours': 10,
    #         'total_price': 100,
    #         'unit_price': 10,
    #         'package': 'sample_package',
    #         'installments': 1,
    #         'email': 'customerOrder@mail.com',
    #         'crm_deal_id': '12345',
    #         'stripe_customer_id': 'cus_test',
    #         'extra_student': 1
    #     }
    #     order = Order.add_new(data=order_data, email_sent=False)
    #     db.session.add(order)
    #     db.session.commit()

    #     assert order.self.mock_data.email == 'customerOrder@mail.com'
    #     assert order.status.value == OrderStatus.PENDING.value

    #     Order.update_order(order.uid, status=OrderStatus.PAID.value)
    #     updated_order = Order.query.get(order.uid)
    #     assert updated_order.self.mock_data.email == 'customerOrder@mail.com'
    #     assert updated_order.status.value == OrderStatus.PAID.value

    #     updated_order = Order.get_order_by_id(order.uid)
    #     assert updated_order.self.mock_data.email == 'customerOrder@mail.com'
    #     assert updated_order.status.value == OrderStatus.PAID.value

    #     Order.get_by_hashed_id(order.hashed_id)
    #     assert updated_order.self.mock_data.email == 'customerOrder@mail.com'
    #     assert updated_order.self.mock_data.package == 'sample_package'

    #     Order.get_customer("cus_test")
    #     assert updated_order.self.mock_data.email == 'customerOrder@mail.com'
    #     assert updated_order.uid == order.uid

    #     old_url = order.stripe_url
    #     Order.update_url(updated_order, "www.test.com")
    #     updated_order = Order.query.get(order.uid)
    #     assert updated_order.self.mock_data.email == 'customerOrder@mail.com'
    #     assert updated_order.stripe_url != old_url

    #     inactive_orders = Order.get_inactive_orders()

    #     Order.update_order(updated_order.uid, active=False)

    #     assert len(inactive_orders) < len(Order.get_inactive_orders())

    #     Order.delete_order(updated_order.uid)
    #     updated_order = Order.get_order_by_id(order.uid)

    #     assert updated_order is None





    def test_add_new_valid_order(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours = 10
        self.mock_data.total_price = 3090
        self.mock_data.package = "12-months-309"
        self.mock_data.installments = 6
        self.mock_data.email = "test@example.com"
        print(self.mock_data.total_hours)
        # Test implementation
        result = Order.add_new(self.mock_data)
        self.assertIs(type(result), type(Order()))

    def test_add_new_invalid_unit_price_negative(self):
        self.mock_data.unit_price = -100
        self.mock_data.total_hours = 10
        self.mock_data.total_price = 1000
        self.mock_data.package = "12-months-100"
        self.mock_data.installments = 6
        self.mock_data.email = "test@example.com"
        # Test implementation
        with self.assertRaises(ValueError):
            # Replace with your actual method call
            Order.add_new(self.mock_data)

    def test_add_new_invalid_unit_price_string(self):
        self.mock_data.unit_price = "invalid"
        self.mock_data.total_hours = 10
        self.mock_data.total_price = 1000
        self.mock_data.package = "12-months-100"
        self.mock_data.installments = 6
        self.mock_data.email = "test@example.com"
        # Test implementation
        with self.assertRaises(ValueError):
            # Replace with your actual method call
            Order.add_new(self.mock_data)

    def test_add_new_invalid_unit_price_zero(self):
        self.mock_data.unit_price = 0
        self.mock_data.total_hours = 10
        self.mock_data.total_price = 0
        self.mock_data.package = "12-months-0"
        self.mock_data.installments = 6
        self.mock_data.email = "test@example.com"
        # Test implementation
        with self.assertRaises(ValueError):
            # Replace with your actual method call
            Order.add_new(self.mock_data)

    def test_add_new_invalid_total_hours_negative(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours = -10
        self.mock_data.total_price = 3090
        self.mock_data.package = "12-months-309"
        self.mock_data.installments = 6
        self.mock_data.email = "test@example.com"
        # Test implementation
        with self.assertRaises(ValueError):
            # Replace with your actual method call
            Order.add_new(self.mock_data)

    def test_add_new_invalid_total_hours_string(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours = "invalid"
        self.mock_data.total_price = 3090
        self.mock_data.package = "12-months-309"
        self.mock_data.installments = 6
        self.mock_data.email = "test@example.com"
        # Test implementation
        with self.assertRaises(ValueError):
            # Replace with your actual method call
            Order.add_new(self.mock_data)

    def test_add_new_invalid_total_hours_zero(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours = 0
        self.mock_data.total_price = 0
        self.mock_data.package = "12-months-0"
        self.mock_data.installments = 6
        self.mock_data.email = "test@example.com"
        # Test implementation
        with self.assertRaises(ValueError):
            # Replace with your actual method call
            Order.add_new(self.mock_data)

    def test_add_new_valid_total_hours_positive(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours = 10
        self.mock_data.total_price = 3090
        self.mock_data.package = "12-months-309"
        self.mock_data.installments = 6
        self.mock_data.email = "test@example.com"
        # Test implementation
        result = Order.add_new(self.mock_data)
        self.assertIs(type(result), type(Order()))

    def test_add_new_invalid_total_price_negative(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours = 10
        self.mock_data.total_price = -3090
        self.mock_data.package = "12-months-309"
        self.mock_data.installments = 6
        self.mock_data.email = "test@example.com"
        # Test implementation
        with self.assertRaises(ValueError):
            # Replace with your actual method call
            Order.add_new(self.mock_data)

    def test_add_new_invalid_total_price_string(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours = 10
        self.mock_data.total_price = "invalid"
        self.mock_data.package = "12-months-309"
        self.mock_data.installments = 6
        self.mock_data.email = "test@example.com"
        # Test implementation
        with self.assertRaises(ValueError):
            # Replace with your actual method call
            Order.add_new(self.mock_data)

    def test_add_new_invalid_total_price_zero(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours = 10
        self.mock_data.total_price = 0
        self.mock_data.package = "12-months-0"
        self.mock_data.installments = 6
        self.mock_data.email = "test@example.com"
        # Test implementation
        with self.assertRaises(ValueError):
            # Replace with your actual method call
            Order.add_new(self.mock_data)

    def test_add_new_valid_total_price_positive(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours = 10
        self.mock_data.total_price = 3090
        self.mock_data.package = "12-months-309"
        self.mock_data.installments = 6
        self.mock_data.email = "test@example.com"
        # Test implementation
        result = Order.add_new(self.mock_data)
        self.assertIs(type(result), type(Order()))

    def test_add_new_valid_package(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours = 10
        self.mock_data.total_price = 3090
        self.mock_data.package = "12-months-309"
        self.mock_data.installments = 6
        self.mock_data.email = "test@example.com"
        # Test implementation
        result = Order.add_new(self.mock_data)
        self.assertIs(type(result), type(Order()))

    def test_add_new_invalid_package_non_string(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours = 10
        self.mock_data.total_price = 3090
        self.mock_data.package = 123
        self.mock_data.installments = 6
        self.mock_data.email = "test@example.com"
        # Test implementation
        with self.assertRaises(ValueError):
            # Replace with your actual method call
            Order.add_new(self.mock_data)

    def test_add_new_invalid_package_empty_string(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours = 10
        self.mock_data.total_price = 3090
        self.mock_data.package = ""
        self.mock_data.installments = 6
        self.mock_data.email = "test@example.com"
        # Test implementation
        with self.assertRaises(ValueError):
            # Replace with your actual method call
            Order.add_new(self.mock_data)

    def test_add_new_invalid_package_long_string(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours = 10
        self.mock_data.total_price = 3090
        self.mock_data.package = "12-months-309-extra"
        self.mock_data.installments = 6
        self.mock_data.email = "test@example.com"
        # Test implementation
        with self.assertRaises(ValueError):
            # Replace with your actual method call
            Order.add_new(self.mock_data)

    def test_add_new_invalid_package_wrong_format(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours =10
        self.mock_data.total_price = 3090
        self.mock_data.package = "invalid-package"
        self.mock_data.installments = 6
        self.mock_data.email = "test@example.com"
        # Test implementation
        with self.assertRaises(ValueError):
            # Replace with your actual method call
            Order.add_new(self.mock_data)

    def test_add_new_invalid_installments_negative(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours =10
        self.mock_data.total_price = 3090
        self.mock_data.package = "12-months-309"
        self.mock_data.installments = -6
        self.mock_data.email = "test@example.com"
        # Test implementation
        with self.assertRaises(ValueError):
            # Replace with your actual method call
            Order.add_new(self.mock_data)

    def test_add_new_invalid_installments_string(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours = 10
        self.mock_data.total_price = 3090
        self.mock_data.package = "12-months-309"
        self.mock_data.installments = "invalid"
        self.mock_data.email = "test@example.com"
        # Test implementation
        with self.assertRaises(ValueError):
            # Replace with your actual method call
            Order.add_new(self.mock_data)

    def test_add_new_invalid_installments_zero(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours = 10
        self.mock_data.total_price = 3090
        self.mock_data.package = "12-months-309"
        self.mock_data.installments = 0
        self.mock_data.email = "test@example.com"
        # Test implementation
        with self.assertRaises(ValueError):
            # Replace with your actual method call
            Order.add_new(self.mock_data)

    def test_add_new_valid_installments(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours =10
        self.mock_data.total_price = 3090
        self.mock_data.package = "12-months-309"
        self.mock_data.installments = 6
        self.mock_data.email = "test@example.com"
        # Test implementation
        result = Order.add_new(self.mock_data)
        self.assertIs(type(result), type(Order()))

    def test_add_new_valid_email(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours = 10
        self.mock_data.total_price = 3090
        self.mock_data.package = "12-months-309"
        self.mock_data.installments = 6
        self.mock_data.email = "test@example.com"
        # Test implementation
        result = Order.add_new(self.mock_data)
        self.assertIs(type(result), type(Order()))

    def test_add_new_invalid_email_long_string(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours =10
        self.mock_data.total_price = 3090
        self.mock_data.package = "12-months-309"
        self.mock_data.installments = 6
        self.mock_data.email = "test" + "a" * 120 + "@example.com"
        # Test implementation
        with self.assertRaises(ValueError):
            # Replace with your actual method call
            Order.add_new(self.mock_data)

    def test_add_new_invalid_email_short_string(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours =10
        self.mock_data.total_price = 3090
        self.mock_data.package = "12-months-309"
        self.mock_data.installments = 6
        self.mock_data.email = "a@example.com"
        # Test implementation
        with self.assertRaises(ValueError):
            # Replace with your actual method call
            Order.add_new(self.mock_data)

    def test_add_new_invalid_email_empty_string(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours =10
        self.mock_data.total_price = 3090
        self.mock_data.package = "12-months-309"
        self.mock_data.installments = 6
        self.mock_data.email = ""
        # Test implementation
        with self.assertRaises(ValueError):
            # Replace with your actual method call
            Order.add_new(self.mock_data)

    def test_add_new_invalid_email_non_string(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours = 10
        self.mock_data.total_price = 3090
        self.mock_data.package = "12-months-309"
        self.mock_data.installments = 6
        self.mock_data.email = 123
        # Test implementation
        with self.assertRaises(ValueError):
            # Replace with your actual method call
            Order.add_new(self.mock_data)




    def test_email_valid_length(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours = 10
        self.mock_data.total_price = 3090
        self.mock_data.package = "12-months-309"
        self.mock_data.installments = 6 
        self.mock_data.email = "test@example.com"
        # Test implementation
        result = Order.add_new(self.mock_data)

        self.assertIs(type(result), type(Order()))

    def test_email_invalid_length_short(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours = 10
        self.mock_data.total_price = 3090
        self.mock_data.package = "12-months-309"
        self.mock_data.installments = 6
        # Test implementation
        self.mock_data.email = "a" * 1 + "@example.com"
        # Test implementation
        with self.assertRaises(ValueError):
            # Replace with your actual method call
            Order.add_new(self.mock_data)

    def test_email_invalid_length_long(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours = 10
        self.mock_data.total_price = 3090
        self.mock_data.package = "12-months-309"
        self.mock_data.installments = 6 
        # Test implementation

        self.mock_data.email = "a" * 121 + "@example.com"
        # Test implementation
        with self.assertRaises(ValueError):
            # Replace with your actual method call
            Order.add_new(self.mock_data)

    def test_unit_price_valid_boundary_lower(self):
        self.mock_data.unit_price = 1
        self.mock_data.total_hours = 10
        self.mock_data.total_price = 3090
        self.mock_data.package = "12-months-309"
        self.mock_data.installments = 6 
        self.mock_data.email = 'test@example.com'
        # Test implementation
        result = Order.add_new(self.mock_data)

        self.assertIs(type(result), type(Order()))

    def test_unit_price_invalid_boundary_lower(self):
        self.mock_data.unit_price = -1
        self.mock_data.total_hours = 10
        self.mock_data.total_price = 3090
        self.mock_data.package = "12-months-309"
        self.mock_data.installments = 6 
        self.mock_data.email = 'test@example.com'

        with self.assertRaises(ValueError):
            # Replace with your actual method call
            Order.add_new(self.mock_data)

    def test_unit_price_valid_boundary_upper(self):
        self.mock_data.unit_price = 100000
        self.mock_data.total_hours = 10
        self.mock_data.total_price = 3090
        self.mock_data.package = "12-months-309"
        self.mock_data.installments = 6 
        self.mock_data.email = 'test@example.com'
        # Test implementation
        result = Order.add_new(self.mock_data)

        self.assertIs(type(result), type(Order()))

    def test_unit_price_invalid_boundary_upper(self):
        self.mock_data.unit_price = -100001
        self.mock_data.total_hours = 10
        self.mock_data.total_price = 3090
        self.mock_data.package = "12-months-309"
        self.mock_data.installments = 6 
        self.mock_data.email = 'test@example.com'

        with self.assertRaises(ValueError):
            Order.add_new(self.mock_data)

    def test_total_hours_valid_boundary_lower(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours = 10
        self.mock_data.total_price = 1
        self.mock_data.package = "12-months-309"
        self.mock_data.installments = 6 
        self.mock_data.email = 'test@example.com'
        # Test implementation
        result = Order.add_new(self.mock_data)
        self.assertIs(type(result), type(Order()))

    def test_total_hours_invalid_boundary_lower(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours = -1
        self.mock_data.total_price = 3090
        self.mock_data.package = "12-months-309"
        self.mock_data.installments = 6 
        self.mock_data.email = 'test@example.com'
        # Test implementation
        with self.assertRaises(ValueError):
            # Replace with your actual method call
            Order.add_new(self.mock_data)

    def test_total_hours_valid_boundary_upper(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours = 100000
        self.mock_data.total_price = 3090
        self.mock_data.package = "12-months-309"
        self.mock_data.installments = 6 
        self.mock_data.email = 'test@example.com'
        # Test implementation
        result = Order.add_new(self.mock_data)
        self.assertIs(type(result), type(Order()))

    def test_total_hours_invalid_boundary_upper(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours = -100000
        self.mock_data.total_price = 3090
        self.mock_data.package = "12-months-309"
        self.mock_data.installments = 6 
        self.mock_data.email = 'test@example.com'
        # Test implementation
        with self.assertRaises(ValueError):
            Order.add_new(self.mock_data)

    def test_total_price_valid_boundary_lower(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours = 10
        self.mock_data.total_price = 1
        self.mock_data.package = "12-months-309"
        self.mock_data.installments = 6 
        self.mock_data.email = 'test@example.com'
        # Test implementation
        result = Order.add_new(self.mock_data)
        self.assertIs(type(result), type(Order()))

    def test_total_price_invalid_boundary_lower(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours = 10
        self.mock_data.total_price = -1
        self.mock_data.package = "12-months-309"
        self.mock_data.installments = 6 
        self.mock_data.email = 'test@example.com'
        # Test implementation
        with self.assertRaises(ValueError):
            # Replace with your actual method call
            Order.add_new(self.mock_data)

    def test_total_price_valid_boundary_upper(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours = 10
        self.mock_data.total_price = 100000
        self.mock_data.package = "12-months-309"
        self.mock_data.installments = 6 
        self.mock_data.email = 'test@example.com'
        # Test implementation
        result = Order.add_new(self.mock_data)
        self.assertIs(type(result), type(Order()))

    def test_total_price_invalid_boundary_upper(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours = -100000
        self.mock_data.total_price = 1
        self.mock_data.package = "12-months-309"
        self.mock_data.installments = 6 
        self.mock_data.email = 'test@example.com'
        with self.assertRaises(ValueError):
            Order.add_new(self.mock_data)

    def test_package_valid_length_lower(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours = 10
        self.mock_data.total_price = 1
        self.mock_data.package = "12-months-309"
        self.mock_data.installments = 6 
        self.mock_data.email ='test@example.com'
        # Test implementation
        result = Order.add_new(self.mock_data)
        self.assertIs(type(result), type(Order()))

    def test_package_invalid_length_lower(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours = 10
        self.mock_data.total_price = 1
        self.mock_data.package = "12-months-30"
        self.mock_data.installments = 6 
        self.mock_data.email ='test@example.com'
        with self.assertRaises(ValueError):
            # Replace with your actual method call
            Order.add_new(self.mock_data)

    def test_package_valid_length_upper(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours = 10
        self.mock_data.total_price = 1
        self.mock_data.package = "12-months-309"
        self.mock_data.installments = 6 
        self.mock_data.email = 'test@example.com'
        # Test implementation
        result = Order.add_new(self.mock_data)
        self.assertIs(type(result), type(Order()))

    def test_package_invalid_length_upper(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours = 10
        self.mock_data.total_price = 1
        self.mock_data.package = "12-months-3091"
        self.mock_data.installments = 6 
        self.mock_data.email = 'test@example.com'
        with self.assertRaises(ValueError):
            Order.add_new(self.mock_data)

    def test_installments_valid_boundary_lower(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours = 10
        self.mock_data.total_price = 1
        self.mock_data.package = "12-months-309"
        self.mock_data.installments = 3
        self.mock_data.email = 'test@example.com'
        # Test implementation
        result = Order.add_new(self.mock_data)
        self.assertIs(type(result), type(Order()))

    def test_installments_invalid_boundary_lower(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours = 10
        self.mock_data.total_price = 1
        self.mock_data.package = "12-months-309"
        self.mock_data.installments = 2 
        self.mock_data.email = 'test@example.com'
        with self.assertRaises(ValueError):
            # Replace with your actual method call
            Order.add_new(self.mock_data)

    def test_installments_valid_boundary_upper(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours = 10
        self.mock_data.total_price = 1
        self.mock_data.package = "12-months-309"
        self.mock_data.installments = 36 
        self.mock_data.email = 'test@example.com'
        # Test implementation
        result = Order.add_new(self.mock_data)
        self.assertIs(type(result), type(Order()))

    def test_installments_invalid_boundary_upper(self):
        self.mock_data.unit_price = 309
        self.mock_data.total_hours = 10
        self.mock_data.total_price = 1
        self.mock_data.package = "12-months-309"
        self.mock_data.installments = 37
        self.mock_data.email = 'test@example.com'

        with self.assertRaises(ValueError):
            # Replace with your actual method call
            Order.add_new(self.mock_data)