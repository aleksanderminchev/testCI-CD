from api.app import db
from api.utils.utils import Updateable, get_date
from models.transaction import CurrencyEnum

from models.order import Order
from models.transaction import Transaction
from flask import abort


class Balance(Updateable, db.Model):  # type:ignore
    """
    The Balance model represents the customer's balance, including orders,
    transactions, and other relevant information such as hours scheduled,
    hours used, hours ordered, and invoice balance.
    """

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(
        db.Integer, db.ForeignKey('customer.id'), index=True)
    customer = db.relationship("Customer", backref="balance", uselist=False)
    orders = db.relationship("Order", backref="balance")
    transactions = db.relationship("Transaction", backref="balance")
    last_updated = db.Column(
        db.DateTime, default=get_date, onupdate=get_date)
    hours_scheduled = db.Column(
        db.Float, default=0, server_default="0", nullable=False)
    hours_free = db.Column(db.Float, default=0,
                           server_default='0', nullable=False)
    hours_used = db.Column(db.Float, default=0,
                           server_default="0", nullable=False)
    hours_ordered = db.Column(
        db.Float, default=0, server_default="0", nullable=False)
    invoice_balance = db.Column(
        db.Float, default=0, server_default="0", nullable=False)
    currency = db.Column(
        db.Enum(
            CurrencyEnum,
            values_callable=lambda obj: [e.value for e in obj]
        ),
        nullable=False,
        default=CurrencyEnum.DKK.value,
        server_default=CurrencyEnum.DKK.value,
    )

    def to_dict(self):
        """
        Convert the balance object to a dictionary.
        """
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "currency": self.currency.value,
            "hours_ordered": self.hours_ordered,
            "hours_scheduled": self.hours_scheduled,
            "hours_used": self.hours_used,
            "hours_free": self.hours_free,
            "invoice_balance": self.invoice_balance,
            "transactions": [i.to_dict() for i in (self.transactions or [])],
            "orders": [i.to_dict() for i in (self.orders or [])],
        }

    # create the initial balance
    # attach the order to the orders here
    # attach the customer
    # add hours_ordered hours
    # create the invoice balance as a minus number for what they have to pay
    # new orders get attached and the  hours_ordered and invoice_balance should increase(for invoice the number goes down)
    # new transactions should be added to the invoice_balance if payment
    # attach transactions to the balance object here
    # for refunds we take the do the same
    @staticmethod
    def create_balance(customer_id, **data):
        from models.customer import Customer
        """
        Creates an empty balance in the DB for new users/customers.
        """
        customer = Customer.get_customer_by_id(customer_id)
        balance = Balance(customer_id=customer.id, **data)
        db.session.add(balance)
        db.session.commit()
        return balance

    # for hours used and scheduled take all of the lessons
    # that the customer(his students) have used
    # take the duration in minutes and divide by 60
    # the add them to the current hours used and scheduled
    # make them seperate methods here
    # where to check if the hours used and scheduled exceed the total amount
    # when we complete a lesson the scheduled number should decrease and the used should increase
    @staticmethod
    def add_order(order_id, customer_id):
        """
        After creating an order in the orders table, attach it to the balance and
        calculate the new hours and total invoice balance.
        """
        order = Order.get_by_hashed_id(order_id)
        balance = Balance.query.filter_by(customer_id=customer_id).first()
        balance.hours_ordered = balance.hours_ordered+order.total_hours

        balance.invoice_balance = balance.invoice_balance-order.total_price
        if order in balance.orders:
            abort(505)
        balance.orders.append(order)
        db.session.add(balance)
        db.session.commit()
        return balance

    @staticmethod
    def remove_order(order_id, customer_id):
        """
        Remove an order from a balance.
        """
        order = Order.get_order_by_id(order_id)
        balance = Balance.query.filter_by(customer_id=customer_id).first()
        balance.hours_ordered = balance.hours_ordered-order.total_hours

        balance.invoice_balance = balance.invoice_balance+order.total_price
        if order not in balance.orders:
            abort(505)
        balance.orders.remove(order)
        db.session.add(balance)
        db.session.commit()
        return balance

    @staticmethod
    def add_transaction(transaction, balance):
        """
        Adds a transaction to the balance.
        """
        if transaction in balance.transactions:
            abort(505)
        if transaction.type_transaction.value == "payment":
            balance.invoice_balance = balance.invoice_balance + transaction.amount
        elif transaction.type_transaction.value == "refund":
            balance.invoice_balance = balance.invoice_balance - transaction.amount
        balance.transactions.append(transaction)
        db.session.add(balance)
        db.session.commit()
        return balance

    @staticmethod
    def remove_transaction(transaction_id, customer_id):
        """
        Removes a transaction from the balance.
        """
        transaction = Transaction.get_transaction_by_id(transaction_id)
        balance = Balance.query.filter_by(customer_id=customer_id).first()
        if transaction not in balance.transactions:
            abort(505)
        if transaction.type_transaction.value == "payment":
            balance.invoice_balance = balance.invoice_balance - transaction.amount
        elif transaction.type_transaction.value == "refund":
            balance.invoice_balance = balance.invoice_balance + transaction.amount
        balance.transactions.remove(transaction)
        db.session.add(balance)
        db.session.commit()
        return balance

    @staticmethod
    def void_order(order):
        """
        Void an order: updates the balance accordingly.
        """
        balance = order.balance
        students = balance.customer.students
        Balance.recalculate_lesson_hours_on_error(students)
        # balance.hours_scheduled=balance.hours_scheduled - order.total_hours
        # balance.hours_used=balance.hours_used - order.total_hours
        balance.hours_ordered = balance.hours_ordered - order.total_hours
        balance.invoice_balance = balance.invoice_balance + order.total_price
        db.session.add(balance)
        db.session.commit()
        return balance

    @staticmethod
    def void_payment_transaction(transaction_id, customer_id):
        """
        Void a payment transaction and update the balance.
        """
        transaction = Transaction.get_transaction_by_id(transaction_id)
        balance = Balance.query.filter_by(customer_id=customer_id).first()

        if transaction not in balance.transactions:
            abort(505)
        if transaction.void:
            abort(505)

        transaction.void = True
        balance.invoice_balance = balance.invoice_balance + transaction.amount
        db.session.add(balance)
        db.session.add(transaction)
        db.session.commit()
        return balance

    @staticmethod
    def unvoid_payment_transaction(transaction_id, customer_id):
        """
        Undo the void of a payment transaction and update the balance.
        """
        transaction = Transaction.get_transaction_by_id(transaction_id)
        balance = Balance.query.filter_by(customer_id=customer_id).first()

        if transaction not in balance.transactions:
            abort(505)
        if not transaction.void:
            abort(505)

        transaction.void = False
        balance.invoice_balance = balance.invoice_balance - transaction.amount
        db.session.add(balance)
        db.session.add(transaction)
        db.session.commit()
        return balance

    # Lessons create scheduled and used hours total
    # optimize array here
    # if we use these methods as part of the finishing of the lesson event
    #  we can just send the lesson and customer objects directly
    @staticmethod
    def use_lesson(lesson_id):
        """
        Update the balance for a used lesson.
        """
        from models.lesson import Lesson
        lesson = Lesson.get_lesson_by_id(lesson_id)
        students = lesson.lessons_students
        lessons = []
        for i in students:
            customer = i.customer
            print(customer.balance[0])
            if lesson in i.lessons:
                customer.balance[0].hours_used = customer.balance[0].hours_used + \
                    (lesson.duration_in_minutes/60)
                hours_check = customer.balance[0].hours_used + \
                    customer.balance[0].hours_scheduled
                if hours_check > customer.balance[0].hours_ordered:
                    abort(
                        500, "Student does not have enough ordered hours to use the lesson")
                customer.balance[0].hours_scheduled = customer.balance[0].hours_scheduled - (
                    lesson.duration_in_minutes/60)
                db.session.add(customer)
                db.session.commit()
        return customer

    @staticmethod
    def schedule_lesson(lesson_id):
        """
        Updates the balance when a student schedules lesson.
        """
        from models.lesson import Lesson
        lesson = Lesson.get_lesson_by_id(lesson_id)
        students = lesson.lessons_students
        lessons = []

        for i in students:
            customer = i.customer
            print(customer.balance)
            if lesson in i.lessons:
                if i.status.value == 'attended':
                    customer.balance[0].hours_used = customer.balance[0].hours_used - (
                        lesson.duration_in_minutes/60)
                customer.balance[0].hours_scheduled = customer.balance[0].hours_scheduled + (
                    lesson.duration_in_minutes/60)

                hours_check = customer.balance[0].hours_used + \
                    customer.balance[0].hours_scheduled
                if hours_check > customer.balance[0].hours_ordered:
                    abort(
                        500, "Student does not have enough ordered hours to use the lesson")
                db.session.add(customer)
                db.session.commit()

        return customer

    @staticmethod
    def cancel_lesson(lesson_id, reason):
        """
        Update the balance for a cancelled lesson based on the cancellation reason.
        """

        from models.lesson import Lesson

        lesson = Lesson.get_lesson_by_id(lesson_id)
        students = lesson.lessons_students

        for i in students:
            customer = i.customer
            if lesson in i.lessons:
                hours_changed = (lesson.duration_in_minutes/60)
                if lesson.status.value == 'scheduled':
                    if reason == 'bad cancellation student':
                        if hours_changed < 2:
                            customer.balance[0].hours_used = customer.balance[0].hours_used + hours_changed
                        else:
                            customer.balance[0].hours_used = customer.balance[0].hours_used + 2
                    elif reason == 'bad cancellation teacher':
                        customer.balance[0].hours_free = customer.balance[0].hours_free + hours_changed

                    customer.balance[0].hours_scheduled = customer.balance[0].hours_scheduled - hours_changed
                elif lesson.status.value == 'attended':
                    if reason == 'bad cancellation student':
                        # maks 2 hours used
                        if hours_changed < 2:
                            customer.balance[0].hours_used += hours_changed
                        else:
                            customer.balance[0].hours_used += 2
                    elif reason == 'bad cancellation teacher':
                        # free hours column maybe
                        customer.balance[0].hours_free = customer.balance[0].hours_free + hours_changed
                        customer.balance[0].hours_used = customer.balance[0].hours_used - hours_changed
                        customer.balance[0].hours_scheduled = customer.balance[0].hours_scheduled - hours_changed

                    elif reason == 'good cancellation':
                        customer.balance[0].hours_used = customer.balance[0].hours_used - hours_changed
                        customer.balance[0].hours_scheduled = customer.balance[0].hours_scheduled - hours_changed
                db.session.add(customer)
                db.session.commit()
        return students[0].customer

    @staticmethod
    def recalculate_lesson_hours_on_error(students):
        """
        Recalculate the lesson hours in case of an error.
        """
        # students=lesson.lessons_students
        hours_total_used = 0
        hours_total_scheduled = 0
        hours_total_free = 0
        for i in students:
            customer = i.customer
            for j in i.lessons:
                duration = (j.duration_in_minutes/60)
                if j.status.value == 'scheduled':
                    hours_total_scheduled += duration
                elif j.status.value == 'attended':
                    hours_total_used += duration
                elif j.status.value == 'bad cancellation student':
                    if duration < 2:
                        hours_total_used += duration
                    else:
                        hours_total_used += 2
                elif j.status.value == 'bad cancellation teacher':
                    hours_total_free += duration
            customer.balance[0].hours_used = hours_total_used
            customer.balance[0].hours_scheduled = hours_total_scheduled
            customer.balance[0].hours_free = hours_total_free
            db.session.add(customer)
            db.session.commit()
            return customer.balance[0]
