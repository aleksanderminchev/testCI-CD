from numbers import Number
from sqlalchemy.orm.session import Session
from sqlalchemy import func
from api.app import db
from api.utils.utils import get_date
from dateutil.relativedelta import relativedelta
import hashlib
import enum
from flask import abort
from models.customer import Customer
from api.utils.utils import Updateable
import itertools
from sqlalchemy.orm import validates
import re
from pprint import pprint
import locale

locale.setlocale(locale.LC_ALL, '')


class OrderStatus(enum.Enum):
    """
    To add this type in migration add:
    from sqlalchemy.dialects import postgresql
    student_status = postgresql.ENUM('pending','paid','void', name='orderstatus')
    student_status.create(op.get_bind())
    """
    PENDING = "pending"
    PAID = "paid"
    VOID = "void"


class Order(Updateable, db.Model):  # type:ignore

    __table__name__ = "Orders"

    uid = db.Column(db.Integer, primary_key=True)
    hashed_id = db.Column(db.String, nullable=True, index=True)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customer.id'), nullable=False, index=True)
    customer = db.relationship('Customer', backref='orders')
    balance_id = db.Column(db.Integer, db.ForeignKey('balance.id'), index=True)
    total_hours = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    # The Stripe ID of the ordered package.
    package = db.Column(db.String, nullable=False)
    # how many monthly installments the package is paid over.
    installments = db.Column(db.Integer, nullable=False)
    crm_deal_id = db.Column(db.String, nullable=True)

    discount = db.Column(db.String, nullable=True)
    stripe_url = db.Column(db.String, nullable=True)
    stripe_customer_id = db.Column(db.String, nullable=True)
    email_sent = db.Column(db.Boolean, default=True,
                           server_default='t', nullable=True)
    # number of extra students
    extra_student = db.Column(db.Integer, nullable=True)
    # if active then the customer has not paid yet. If inactive,
    # then the customer has paid.
    active = db.Column(db.Boolean, default=True, nullable=False, index=True)
    status = db.Column(
        db.Enum(
            OrderStatus,
            values_callable=lambda obj: [e.value for e in obj]
        ),
        nullable=False,
        default=OrderStatus.PENDING.value,
        server_default=OrderStatus.PENDING.value,
        index=True
    )
    created_at = db.Column(db.DateTime, default=get_date)
    last_updated = db.Column(
        db.DateTime, default=get_date, onupdate=get_date)
    expiration_date = db.Column(db.DateTime, nullable=True)
    void_date = db.Column(db.DateTime, nullable=True)
    expired = db.Column(db.Boolean, default=False)
    booking_date = db.Column(db.DateTime, nullable=True)
    upsell = db.Column(db.Boolean, default=False)
    teachworks_id = db.Column(db.Integer, nullable=True)

    @validates("total_hours")
    def validate_total_hours(self, key, total_hours):
        if not isinstance(total_hours, Number):
            raise ValueError("invalid total hours")
        if total_hours <= 0:
            raise ValueError("invalid total hours")
        return total_hours

    @validates("total_price")
    def validate_total_price(self, key, total_price):
        if not isinstance(total_price, Number):
            raise ValueError("invalid total price")
        if total_price <= 0:
            raise ValueError("invalid total price")
        return total_price

    @validates("unit_price")
    def validate_unit_price(self, key, unit_price):
        if not isinstance(unit_price, Number):
            raise ValueError("invalid unit price")
        if unit_price <= 0:
            raise ValueError("invalid unit price")
        return unit_price

    @validates("email")
    def validate_email(self, key, email):
        if not isinstance(email, str):
            raise ValueError("invalid email")
        if 12 >= len(email) >= 120:
            raise ValueError("invalid email")

    @validates("installments")
    def validate_installments(self, key, installments):
        if not isinstance(installments, Number):
            raise ValueError("invalid installments")
        if 36 < installments or installments < 3:
            raise ValueError("invalid installments")
        return installments

    @validates("package")
    def validate_package(self, key, package):
        if not isinstance(package, str):
            raise ValueError("invalid package")
        if len(package) != 13:
            raise ValueError("invalid package")
        if not re.match(r"^\d{2}-months-\d{3}$", package):
            raise ValueError("invalid package")
        return package

    @staticmethod
    def add_new(data, email_sent=True, session=None):
        order = Order()
        order.total_hours = data.total_hours
        order.total_price = data.total_price
        order.unit_price = data.unit_price
        order.package = data.package
        order.installments = data.installments
        order.email = data.email
        order.email_sent = email_sent
        order.crm_deal_id = data.crm_deal_id
        if data.discount is not None:
            order.discount = data.discount
        order.stripe_customer_id = data.stripe_customer_id
        order.extra_student = data.extra_student

        order.upsell = data.upsell
        # making the relationship to the customer
        internal_customer = Customer.get_customer_by_email(order.email)

        if internal_customer is None:
            raise ValueError(
                'Error creating order: Customer not found på email.')
        order.customer_id = internal_customer.customer.id
        if session is None:
            db.session.add(order)
            db.session.commit()
            order.set_expiration_date()
            uid_hash = str(order.uid) + str(order.crm_deal_id)
            uid_hash = uid_hash.encode('utf-8')
            order.hashed_id = hashlib.sha224(uid_hash).hexdigest()

            db.session.commit()
        else:
            session.add(order)
            session.commit()
            order.set_expiration_date()
            uid_hash = str(order.uid) + str(order.crm_deal_id)
            uid_hash = uid_hash.encode('utf-8')
            order.hashed_id = hashlib.sha224(uid_hash).hexdigest()

            session.commit()
        return order

    def set_expiration_date(self):
        unit_price = self.unit_price
        today = self.created_at
        expiration_mapping = {
            399: today + relativedelta(months=+3),
            309: today + relativedelta(months=+6),
            289: today + relativedelta(months=+12),
            269: today + relativedelta(months=+18),
            249: today + relativedelta(months=+24),
            229: today + relativedelta(months=+36)
        }

        self.expiration_date = expiration_mapping.get(
            unit_price, today + relativedelta(months=+3))

    def to_dict(self):
        return {
            "id": self.uid,
            "customer_id": self.customer_id,
            "name": f'{self.customer.user.first_name} {self.customer.user.last_name}',
            "hashed_id": self.hashed_id,
            "total_hours": self.total_hours,
            "total_price": self.total_price,
            "unit_price": self.unit_price,
            "type_order": self.package,
            "installments": self.installments,
            "crm_deal_id": self.crm_deal_id,
            "discount": self.discount,
            "email_sent": self.email_sent,
            "stripe_url": self.stripe_url,
            "stripe_customer_id": self.stripe_customer_id,
            "extra_student": self.extra_student,
            "active": self.active,
            "status": self.status.value,
            "last_updated": self.last_updated,
            "expiration_date": self.expiration_date,
            "created_at": self.created_at
        }

    @staticmethod
    def get_query_of_all_orders(session: Session = None):
        if session is None:
            return Order.query.all()
        else:
            return session.query(Order)

    @staticmethod
    def get_order_by_id(id):
        return Order.query.get(id)

    @staticmethod
    def get_inactive_orders():
        return Order.query.filter_by(active=False).all()

    @staticmethod
    def update_order(uid=int, **kwargs):
        """Updates a order by the User id from the DB"""
        order_query = Order.query.get(uid)
        Order.update(order_query, kwargs)
        db.session.commit()
        return order_query

    @staticmethod
    def delete_order(id):
        """Deletes a order from the DB"""
        order = Order.query.get(id) or abort(404)
        order_for_return = order.to_dict()
        db.session.delete(order)
        db.session.commit()
        return order_for_return

    @staticmethod
    def get_by_hashed_id(hashed_id):
        """ Gets order with given hashed_id. """
        return Order.query.filter_by(hashed_id=hashed_id).first()

    @staticmethod
    def get_customer(stripe_customer_id):
        """ Gets Order row with given stripe id"""
        return Order.query.filter_by(
            stripe_customer_id=stripe_customer_id
        ).first()

    def update_url(self, data, session: Session = None):
        self.stripe_url = data
        if session is None:
            db.session.commit()
        else:
            session.commit()

    def update_status(self, data, session: Session = None):
        self.active = data
        self.status = 'paid'
        if session is None:
            db.session.commit()
        else:
            session.commit()

    def dump(self):
        print(f"{self.uid} {self.hashed_id} {self.total_hours} {self.total_price} {self.unit_price} {self.package} {self.installments} {self.crm_deal_id} {self.discount} {self.discount} {self.stripe_url}")

    # Data extraction:

    @staticmethod
    def booking_sum():
        """Queries the database to extract all of the bookings that have the same month and year
           afterwards it groups them together, and calcualates the total_sum, amount of paid bookings
           in that corresponding year and month, the average of total_price.
        """
        result = db.session.query(
            func.date_trunc("month", Order.booking_date).label("month_year"),
            func.sum(Order.total_price).label("sum"),
            func.count(Order.uid).label("count"),
            func.avg(Order.total_price).label("avg_price")
        ).filter(
            Order.booking_date != None
        ).group_by(
            func.date_trunc("month", Order.booking_date)
        ).all()

        upsell = db.session.query(
            func.date_trunc("month", Order.booking_date).label("month_year"),
            func.sum(Order.total_price).label("sum"),
            func.count(Order.uid).label("count"),
            func.avg(Order.total_price).label("avg_price")
        ).filter(
            Order.booking_date != None,
            Order.upsell == True
        ).group_by(
            func.date_trunc("month", Order.booking_date)
        ).all()

        new = db.session.query(
            func.date_trunc("month", Order.booking_date).label("month_year"),
            func.sum(Order.total_price).label("sum"),
            func.count(Order.uid).label("count"),
            func.avg(Order.total_price).label("avg_price")
        ).filter(
            Order.booking_date != None,
            Order.upsell == False
        ).group_by(
            func.date_trunc("month", Order.booking_date)
        ).all()

        formatted_result = [
            {
                "date": month_year,
                "total_total": locale.format_string("%.0f", total_sum, grouping=True),
                "total_amount_of_bookings": count,
                "total_average": locale.format_string("%.0f", avg_price, grouping=True)
            }
            for month_year, total_sum, count, avg_price in result
        ]

        formatted_result_upsell = [
            {
                "date": month_year,
                "upsell_total": locale.format_string("%.0f", total_sum, grouping=True),
                "upsell_amount_of_bookings": count,
                "upsell_average": locale.format_string("%.0f", avg_price, grouping=True)
            }
            for month_year, total_sum, count, avg_price in upsell
        ]

        formatted_result_new = [
            {
                "date": month_year,
                "new_total": locale.format_string("%.0f", total_sum, grouping=True),
                "new_amount_of_bookings": count,
                "new_average": locale.format_string("%.0f", avg_price, grouping=True)
            }
            for month_year, total_sum, count, avg_price in new
        ]

        combined_result = []
        for a, b, c in itertools.zip_longest(formatted_result,
                                             formatted_result_upsell,
                                             formatted_result_new, fillvalue={}):
            combined_dict = {**a, **b, **c}
            combined_result.append(combined_dict)

        return combined_result

    @staticmethod
    def circle_diagrams():
        result = db.session.query(
            func.date_trunc("month", Order.booking_date).label("month_year"),
            Order.package,
            func.count(Order.package).label("count")
        ).filter(
            Order.booking_date != None
        ).group_by(
            Order.package,  # include package in GROUP BY clause
            func.date_trunc("month", Order.booking_date)
        ).all()

        formatted_result = {}
        for month_year, package, count in result:
            month_date = month_year.date()  # convert datetime.datetime to date
            month_dict = formatted_result.get(month_date, {})
            month_dict[package] = count
            formatted_result[month_date] = month_dict

        return formatted_result
