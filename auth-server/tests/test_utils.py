from numbers import Number
from api.app import db
from tests.base_test_case import BaseTestCase
from models.order import Order, OrderStatus
from models.customer import Customer
from unittest.mock import Mock
from datetime import datetime
import pandas as pd
from api.utils.accounting import calculate_balances, calculate_average_hourly_price,\
    calculate_net_payment, calculate_revenue_generated, get_accrued_hours


class UtilsTestCase(BaseTestCase):

    def setUp(self):
        # user_teacher = User(email='teacher@test.com', password='foo')
        self.student = Order()
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

    def test_calculate_revenue_generated_valid_start_date(self):
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 2, 2)
        # Test implementation
        self.assertIsInstance(
            calculate_revenue_generated(start_date, end_date), list)

    def test_calculate_revenue_generated_invalid_start_date_non_date_input(self):
        start_date = "2023-01-01"
        end_date = datetime(2023, 2, 2)
        # Test implementation
        with self.assertRaises(ValueError):
            calculate_revenue_generated(start_date, end_date)

    def test_calculate_revenue_generated_invalid_start_date_zero(self):
        start_date = 0
        end_date = datetime(2023, 2, 2)
        # Test implementation
        with self.assertRaises(ValueError):
            calculate_revenue_generated(start_date, end_date)

    def test_calculate_revenue_generated_valid_end_datetime(self):
        start_date = datetime(2023, 2, 2)
        end_date = datetime(2023, 12, 31)
        # Test implementation
        self.assertIsInstance(
            calculate_revenue_generated(start_date, end_date), list)

    def test_calculate_revenue_generated_invalid_end_date_non_date_input(self):
        start_date = datetime(2023, 2, 2)
        end_date = "2023-12-31"
        # Test implementation
        with self.assertRaises(ValueError):
            calculate_revenue_generated(start_date, end_date)

    def test_calculate_revenue_generated_invalid_end_date_zero(self):
        start_date = datetime(2023, 2, 2)
        end_date = 0
        # Test implementation
        with self.assertRaises(ValueError):
            calculate_revenue_generated(start_date, end_date)

    def test_calculate_revenue_generated_invalid_data_zero(self):
        start_date = datetime(2023, 2, 2)
        data = 0
        # Test implementation
        with self.assertRaises(ValueError):
            calculate_revenue_generated(start_date, data)

    def test_calculate_revenue_generated_valid_data_dataframe_type(self):
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 2, 2)
        # Test implementation
        self.assertIsInstance(
            calculate_revenue_generated(start_date, end_date), list)

    def test_calculate_revenue_generated_valid_data_dataframe_length_zero(self):
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 2, 2)
        # Test implementation
        self.assertEqual(
            len(calculate_revenue_generated(start_date, end_date)), 0)

    def test_calculate_revenue_generated_invalid_data_non_dataframe_type(self):
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 2, 2)
        # Test implementation
        self.assertNotIsInstance(
            calculate_revenue_generated(start_date, end_date), Number)

    def test_calculate_revenue_generated_invalid_start_date_null(self):
        start_date = None
        end_date = datetime(2023, 2, 2)
        # Test implementation
        with self.assertRaises(ValueError):
            calculate_revenue_generated(start_date, end_date)

    def test_calculate_revenue_generated_invalid_end_date_null(self):
        start_date = datetime(2023, 1, 1)
        end_date = None
        # Test implementation
        with self.assertRaises(ValueError):
            calculate_revenue_generated(start_date, end_date)

    def test_calculate_balances_valid_date_not_null(self):
        date = datetime(2023, 1, 1)
        # Test implementation
        self.assertIsInstance(calculate_balances(date), list)

    def test_calculate_balances_invalid_date_null(self):
        date = None
        # Test implementation
        with self.assertRaises(ValueError):
            calculate_balances(date)

    def test_calculate_balances_invalid_date_non_date_type(self):
        date = "2023-01-01"
        # Test implementation
        with self.assertRaises(ValueError):
            calculate_balances(date)

    def test_calculate_balances_invalid_date_zero(self):
        date = 0
        # Test implementation
        with self.assertRaises(ValueError):
            calculate_balances(date)

    def test_calculate_balances_invalid_data_zero(self):
        date = datetime(2023, 1, 1)
        # Test implementation
        self.assertNotEqual(calculate_balances(date), 0)

    def test_calculate_balances_valid_data_dataframe_type(self):
        date = datetime(2023, 1, 1)
        # Test implementation
        self.assertIsInstance(calculate_balances(date), list)

    def test_calculate_balances_valid_data_dataframe_length_zero(self):
        date = datetime(2023, 1, 1)
        # Test implementation
        self.assertEqual(len(calculate_balances(date)), 0)

    def test_calculate_balances_invalid_data_non_dataframe_type(self):
        data = "data"
        date = datetime(2023, 1, 1)
        # Test implementation
        self.assertNotEqual(calculate_balances(date), data)
        self.assertNotIsInstance(calculate_balances(date), str)

    def test_calculate_net_payment_valid_customer_not_null(self):
        customer = self.customer
        date = datetime(2023, 1, 1)
        # Test implementation
        self.assertIsInstance(calculate_net_payment(customer, date), Number)

    def test_calculate_net_payment_invalid_customer_zero(self):
        customer = 0
        date = datetime(2023, 1, 1)
        # Test implementation
        with self.assertRaises(ValueError):
            calculate_net_payment(customer, date)

    def test_calculate_net_payment_invalid_customer_null(self):
        customer = None
        date = datetime(2023, 1, 1)
        # Test implementation
        with self.assertRaises(ValueError):
            calculate_net_payment(customer, date)

    def test_calculate_net_payment_invalid_date_zero(self):
        customer = self.customer
        date = 0
        # Test implementation
        with self.assertRaises(ValueError):
            calculate_net_payment(customer, date)

    def test_calculate_net_payment_valid_date_not_null(self):
        date = datetime(2023, 1, 1)
        customer = self.customer
        # Test implementation
        self.assertIsInstance(calculate_net_payment(customer, date), Number)

    def test_calculate_net_payment_invalid_date_non_date_type(self):
        date = "2023-01-01"
        customer = self.customer
        # Test implementation
        with self.assertRaises(ValueError):
            calculate_net_payment(customer, date)

    def test_calculate_net_payment_valid_hours_zero(self):
        customer = self.customer
        date = datetime(2023, 1, 1)
        # Test implementation
        self.assertEqual(calculate_net_payment(customer, date), 0.0)

    def test_calculate_net_payment_valid_hours_positive(self):
        customer = self.customer
        date = datetime(2023, 1, 1)
        # Test implementation
        self.assertIsInstance(calculate_net_payment(customer, date), Number)

    def test_calculate_net_payment_invalid_hours_negative(self):
        customer = self.customer
        date = datetime(2023, 1, 1)
        # Test implementation
        self.assertNotEqual(calculate_net_payment(customer, date), -5)

    def test_calculate_average_hourly_price_valid_customer_not_null(self):
        customer = self.customer
        date = datetime(2023, 1, 1)
        # Test implementation
        self.assertIsInstance(calculate_average_hourly_price(
            customer, date)['average_hourly_price'], Number)

    def test_calculate_average_hourly_price_invalid_customer_zero(self):
        customer = 0
        date = datetime(2023, 1, 1)
        # Test implementation
        with self.assertRaises(ValueError):
            calculate_average_hourly_price(customer, date)

    def test_calculate_average_hourly_price_invalid_customer_null(self):
        customer = None
        date = datetime(2023, 1, 1)
        # Test implementation
        with self.assertRaises(ValueError):
            calculate_average_hourly_price(customer, date)

    def test_calculate_average_hourly_price_invalid_date_zero(self):
        customer = self.customer
        date = 0
        # Test implementation
        with self.assertRaises(ValueError):
            calculate_average_hourly_price(customer, date)

    def test_calculate_average_hourly_price_valid_date_not_null(self):
        date = datetime(2023, 1, 1)
        customer = self.customer
        # Test implementation
        self.assertIsInstance(calculate_average_hourly_price(
            customer, date)['average_hourly_price'], Number)

    def test_calculate_average_hourly_price_invalid_date_non_date_type(self):
        date = "2023-01-01"
        customer = self.customer
        # Test implementation
        with self.assertRaises(ValueError):
            calculate_average_hourly_price(customer, date)

    def test_calculate_average_hourly_price_valid_hours_zero(self):
        customer = self.customer
        date = datetime(2023, 1, 1)
        # Test implementation
        self.assertEqual(calculate_average_hourly_price(
            customer, date)['average_hourly_price'], 0.0)

    def test_calculate_average_hourly_price_valid_hours_positive(self):
        customer = self.customer
        date = datetime(2023, 1, 1)
        # Test implementation
        self.assertIsInstance(calculate_average_hourly_price(
            customer, date)['average_hourly_price'], Number)

    def test_calculate_average_hourly_price_invalid_hours_negative(self):
        customer = self.customer
        date = datetime(2023, 1, 1)
        # Test implementation
        self.assertNotEqual(calculate_average_hourly_price(
            customer, date)['average_hourly_price'], -5)

    def test_get_accrued_hours_valid_customer_not_null(self):
        customer = self.customer
        date = datetime(2023, 1, 1)
        # Test implementation
        self.assertIsInstance(get_accrued_hours(customer, date), Number)

    def test_get_accrued_hours_invalid_customer_zero(self):
        customer = 0
        date = datetime(2023, 1, 1)
        # Test implementation
        with self.assertRaises(ValueError):
            get_accrued_hours(customer, date)

    def test_get_accrued_hours_invalid_customer_null(self):
        customer = None
        date = datetime(2023, 1, 1)
        # Test implementation
        with self.assertRaises(ValueError):
            get_accrued_hours(customer, date)

    def test_get_accrued_hours_invalid_date_zero(self):
        customer = self.customer
        date = 0
        # Test implementation
        with self.assertRaises(ValueError):
            get_accrued_hours(customer, date)

    def test_get_accrued_hours_valid_date_not_null(self):
        date = datetime(2023, 1, 1)
        customer = self.customer
        # Test implementation
        self.assertIsInstance(get_accrued_hours(customer, date), Number)

    def test_get_accrued_hours_invalid_date_non_date_type(self):
        date = "2023-01-01"
        customer = self.customer
        # Test implementation
        with self.assertRaises(ValueError):
            get_accrued_hours(customer, date)

    def test_get_accrued_hours_valid_hours_zero(self):
        customer = self.customer
        date = datetime(2023, 1, 1)
        # Test implementation
        self.assertEqual(get_accrued_hours(customer, date), 0.0)

    def test_get_accrued_hours_valid_hours_positive(self):
        customer = self.customer
        date = datetime(2023, 1, 1)
        # Test implementation
        self.assertIsInstance(get_accrued_hours(customer, date), Number)

    def test_get_accrued_hours_invalid_hours_negative(self):
        customer = self.customer
        date = datetime(2023, 1, 1)
        # Test implementation
        self.assertNotEqual(get_accrued_hours(customer, date), -5)
