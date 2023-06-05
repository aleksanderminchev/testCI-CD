import pytest
from api.app import db
from api.utils.utils import datetime
from models.balance import Balance
from tests.base_test_case import BaseTestCase
from models.customer import Customer
from models.user import User
from models.order import Order


class BalanceModelTestCases(BaseTestCase):
    def setUp(self):
        print("Setting up local")
        # Creating an independent customer with an empty Balance.
        customer = Customer.add_independent_customer_with_student(
            'balances@mail.com', '123', 'Independt', 'Last name', '12312',)

        Balance.create_balance(
            customer_id=customer['customer'].id, hours_scheduled=10, hours_used=0, hours_ordered=20, invoice_balance=0, currency='DKK')

        order = Order(hashed_id='12312', total_hours=12, total_price=12312,
                      unit_price=12, package='string',
                      installments=2, crm_deal_id='2',
                      discount='strin312', stripe_customer_id="dasd",
                      stripe_url='fweweew', extra_student=1, customer_id=customer['customer'].id)

        db.session.add(order)
        db.session.commit()
        Balance.add_order(order.uid, customer['customer'].id)
        super().setUp()

    def tearDown(self):
        customer = Customer.get_customer_by_email('balances@mail.com').customer
        print(customer.balance)
        print(customer.balance[0].hours_used)
        for i in customer.balance:
            customer.balance.remove(i)
            db.session.delete(i)
            db.session.commit()
        for i in customer.students:
            for j in i.lessons:
                db.session.delete(j)
            # db.session.delete(i.lessons)
        # customer.balance[0] =Balance(customer_id=customer.id,hours_scheduled=10,hours_used=0,hours_ordered=20,invoice_balance=0,currency='DKK')
        print(customer.balance)

        db.session.add(customer)
        db.session.commit()
        super().tearDown()

    def test_balance_init(self):
        customer = User.find_by_email("balances@mail.com")
        balance = Balance(
            customer_id=customer.id,
            hours_scheduled=2,
            hours_used=0,
            hours_ordered=12,
            invoice_balance=0,
            currency='DKK'
        )
        assert balance.customer_id == customer.id
        assert balance.hours_scheduled == 2
        assert balance.hours_used == 0
        assert balance.hours_ordered == 12
        assert balance.invoice_balance == 0
        assert balance.currency == 'DKK'

    # def test_add_order(self):
    #     customer = Customer.get_customer_by_id(1)
    #     old_hours = customer.balance[0].hours_ordered
    #     old_invoice = customer.balance[0].invoice_balance
    #     order = Order(hashed_id='12312', total_hours=12, total_price=12312,
    #                   unit_price=12, package='string',
    #                   installments=2, crm_deal_id='2',
    #                   discount='strin312', stripe_customer_id="dasd",
    #                   stripe_url='fweweew', extra_student=1, customer_id=customer.id)
    #     print(order)
    #     db.session.add(order)
    #     db.session.commit()
    #     balance = Balance.add_order(order.uid, 1)
    #     assert order in balance.orders
    #     assert balance.hours_ordered == old_hours+order.total_hours
    #     assert balance.invoice_balance == old_invoice-order.total_price

    # def test_remove_order(self):
    #     customer = Customer.get_customer_by_id(1)
    #     old_hours = customer.balance[0].hours_ordered
    #     order = customer.balance[0].orders[0]
    #     balance = Balance.remove_order(order.uid, customer.id)
    #     assert order not in balance.orders
    #     assert old_hours != balance.hours_ordered-order.total_hours
    #     assert balance.invoice_balance != 0-order.total_price
    # # test for payment
    # # test for refund
    # # test for void and unvoid

    # def test_add_payment_transaction(self):
    #     from models.transaction import Transaction
    #     customer = Customer.get_customer_by_id(1)
    #     transaction = Transaction(
    #         customer_id=customer.id, stripe_transaction_id="312310", amount=200)
    #     db.session.add(transaction)
    #     db.session.commit()
    #     initial_balance = customer.balance[0].invoice_balance
    #     transactions = customer.balance[0].add_transaction(
    #         transaction_id=transaction.id, customer_id=customer.id)
    #     assert transaction in customer.balance[0].transactions
    #     assert Transaction.get_transaction_by_id(transaction.id) == transaction
    #     assert initial_balance + \
    #         transaction.amount == customer.balance[0].invoice_balance

    # def test_remove_payment_transaction(self):
    #     from models.transaction import Transaction
    #     customer = Customer.get_customer_by_id(1)
    #     transaction = Transaction(
    #         customer_id=customer.id, balance_id=customer.balance[0].id, stripe_transaction_id="312310", amount=200)
    #     db.session.add(transaction)
    #     db.session.commit()
    #     initial_balance = customer.balance[0].invoice_balance
    #     new_balance = customer.balance[0].remove_transaction(
    #         transaction_id=transaction.id, customer_id=customer.id)
    #     assert transaction not in customer.balance[0].transactions
    #     assert Transaction.get_transaction_by_id(transaction.id) == transaction
    #     assert initial_balance - \
    #         transaction.amount == customer.balance[0].invoice_balance

    # def test_add_refund_transaction(self):
    #     from models.transaction import Transaction
    #     customer = Customer.get_customer_by_id(1)
    #     transaction = Transaction(
    #         customer_id=customer.id, stripe_transaction_id="312310", amount=200, type_transaction="refund")
    #     db.session.add(transaction)
    #     db.session.commit()
    #     initial_balance = customer.balance[0].invoice_balance
    #     transactions = customer.balance[0].add_transaction(
    #         transaction_id=transaction.id, customer_id=customer.id)
    #     assert transaction in customer.balance[0].transactions
    #     assert Transaction.get_transaction_by_id(transaction.id) == transaction
    #     assert initial_balance - \
    #         transaction.amount == customer.balance[0].invoice_balance

    # def test_remove_refund_transaction(self):
    #     from models.transaction import Transaction
    #     customer = Customer.get_customer_by_id(1)
    #     transaction = Transaction(
    #         customer_id=customer.id, balance_id=customer.balance[0].id, stripe_transaction_id="312310", type_transaction='refund', amount=200)
    #     db.session.add(transaction)
    #     db.session.commit()
    #     initial_balance = customer.balance[0].invoice_balance
    #     new_balance = customer.balance[0].remove_transaction(
    #         transaction_id=transaction.id, customer_id=customer.id)
    #     assert transaction not in customer.balance[0].transactions
    #     assert Transaction.get_transaction_by_id(transaction.id) == transaction
    #     assert initial_balance + \
    #         transaction.amount == customer.balance[0].invoice_balance

    # def test_void_transaction(self):
    #     from models.transaction import Transaction
    #     customer = Customer.get_customer_by_id(1)
    #     transaction = Transaction(
    #         customer_id=customer.id, balance_id=customer.balance[0].id, stripe_transaction_id="312310", amount=200, type_transaction="refund")
    #     db.session.add(transaction)
    #     db.session.commit()
    #     initial_balance = customer.balance[0].invoice_balance
    #     new_balance = customer.balance[0].void_payment_transaction(
    #         transaction.id, customer.id)
    #     assert transaction.void
    #     assert Transaction.get_transaction_by_id(transaction.id) == transaction
    #     assert initial_balance + \
    #         transaction.amount == customer.balance[0].invoice_balance

    # def test_unvoid_transaction(self):
    #     from models.transaction import Transaction
    #     customer = Customer.get_customer_by_id(1)
    #     transaction = Transaction(
    #         customer_id=customer.id, balance_id=customer.balance[0].id, stripe_transaction_id="312310", void=True, amount=200)
    #     db.session.add(transaction)
    #     db.session.commit()
    #     initial_balance = customer.balance[0].invoice_balance
    #     new_balance = customer.balance[0].unvoid_payment_transaction(
    #         transaction.id, customer.id)

    #     assert not transaction.void
    #     assert Transaction.get_transaction_by_id(transaction.id) == transaction
    #     assert initial_balance - \
    #         transaction.amount == customer.balance[0].invoice_balance

    # def test_use_lesson(self):
    #     from models.lesson import Lesson
    #     from models.student import Student
    #     from models.teacher import Teacher
    #     customer = Customer.get_customer_by_email('test@test.com')
    #     student = Student.get_student_by_id(1)
    #     teacher = Teacher.get_teacher_by_id(1)
    #     lesson = Lesson(teacher_id=teacher.id, space="dsaeevv", from_time=datetime.datetime(2023, 5, 15, 16, 00),
    #                     to_time=datetime.datetime(2023, 5, 15, 18, 00), status='attended', duration_in_minutes=120, wage=240)
    #     lesson.lessons_students.append(student)
    #     db.session.add(lesson)
    #     db.session.commit()
    #     new_customer = customer.balance[0].use_lesson(lesson.id)
    #     db.session.add(customer)
    #     db.session.commit()
    #     assert new_customer.balance[0].hours_used == 2
    #     assert new_customer.balance[0].hours_scheduled == 8

    # def test_schedule_lesson(self):
    #     from models.lesson import Lesson
    #     from models.student import Student
    #     from models.teacher import Teacher
    #     customer = Customer.get_customer_by_email('test@test.com')

    #     student = Student.get_student_by_id(1)
    #     teacher = Teacher.get_teacher_by_id(1)
    #     lesson = Lesson(teacher_id=teacher.id, space="dsaeevv", from_time=datetime.datetime(2023, 5, 17, 16, 00),
    #                     to_time=datetime.datetime(2023, 5, 17, 18, 00), status='scheduled', duration_in_minutes=120, wage=240)
    #     lesson.lessons_students.append(student)
    #     db.session.add(lesson)
    #     db.session.commit()
    #     new_customer = customer.balance[0].schedule_lesson(lesson.id)
    #     db.session.add(customer)
    #     db.session.commit()
    #     assert new_customer.balance[0].hours_used == 0
    #     assert new_customer.balance[0].hours_scheduled == 12
    # # registers lesson

    # def test_cancel_lesson(self):
    #     from models.lesson import Lesson
    #     from models.teacher import Teacher
    #     customer = Customer.get_customer_by_email('test@test.com')
    #     student = customer.students[0]
    #     teacher = Teacher.get_teacher_by_id(1)
    #     lesson = Lesson(teacher_id=teacher.id, space="dsaeevv", from_time=datetime.datetime(2023, 5, 16, 16, 00),
    #                     to_time=datetime.datetime(2023, 5, 16, 18, 00), status='scheduled', duration_in_minutes=120, wage=240)
    #     lesson.lessons_students.append(student)
    #     db.session.add(lesson)
    #     db.session.commit()
    #     new_customer = customer.balance[0].cancel_lesson(
    #         lesson_id=lesson.id, reason="good cancellation")
    #     db.session.add(customer)
    #     db.session.commit()
    #     assert new_customer
    #     assert customer.balance[0].hours_used == 0
    #     assert customer.balance[0].hours_scheduled == 8

    # # registers lesson
    # def test_cancel_bad_teacher_lesson(self):
    #     from models.lesson import Lesson
    #     from models.teacher import Teacher
    #     customer = Customer.get_customer_by_email('test@test.com')
    #     student = customer.students[0]
    #     teacher = Teacher.get_teacher_by_id(1)
    #     lesson = Lesson(teacher_id=teacher.id, space="dsaeevv", from_time=datetime.datetime(2023, 5, 16, 16, 00),
    #                     to_time=datetime.datetime(2023, 5, 16, 18, 00), status='scheduled', duration_in_minutes=120, wage=240)
    #     lesson.lessons_students.append(student)
    #     db.session.add(lesson)
    #     db.session.commit()
    #     new_customer = customer.balance[0].cancel_lesson(
    #         lesson_id=lesson.id, reason="bad cancellation teacher")
    #     db.session.add(customer)
    #     db.session.commit()
    #     assert new_customer
    #     assert customer.balance[0].hours_used == 0
    #     assert customer.balance[0].hours_scheduled == 8

    # def test_cancel_bad_student_lesson(self):
    #     from models.lesson import Lesson
    #     from models.teacher import Teacher
    #     customer = Customer.get_customer_by_email('test@test.com')
    #     student = customer.students[0]
    #     teacher = Teacher.get_teacher_by_id(1)
    #     lesson = Lesson(teacher_id=teacher.id, space="dsaeevv", from_time=datetime.datetime(2023, 5, 16, 16, 00),
    #                     to_time=datetime.datetime(2023, 5, 16, 19, 00), status='scheduled', duration_in_minutes=180, wage=240)
    #     lesson.lessons_students.append(student)
    #     db.session.add(lesson)
    #     db.session.commit()
    #     new_customer = customer.balance[0].cancel_lesson(
    #         lesson_id=lesson.id, reason="bad cancellation student")
    #     db.session.add(customer)
    #     db.session.commit()
    #     assert new_customer
    #     assert customer.balance[0].hours_scheduled == 7
    #     assert customer.balance[0].hours_used == 2

    # def test_recalculate_balance(self):
    #     from models.lesson import Lesson
    #     from models.teacher import Teacher
    #     customer = Customer.get_customer_by_email('test@test.com')
    #     student = customer.students[0]
    #     teacher = Teacher.get_teacher_by_id(1)
    #     lesson = Lesson(teacher_id=teacher.id, space="dsaeevv", from_time=datetime.datetime(2023, 5, 16, 16, 00),
    #                     to_time=datetime.datetime(2023, 5, 16, 19, 00), status='scheduled', duration_in_minutes=180, wage=240)
    #     lesson.lessons_students.append(student)
    #     db.session.add(lesson)
    #     db.session.commit()
    #     hours_scheduled_before_recalculation = customer.balance[0].hours_scheduled
    #     hours_used_before_recalculation = customer.balance[0].hours_used
    #     customer.balance[0].recalculate_lesson_hours_on_error(lesson)
    #     assert customer.balance[0].hours_scheduled != hours_scheduled_before_recalculation
    #     assert customer.balance[0].hours_used == hours_used_before_recalculation
