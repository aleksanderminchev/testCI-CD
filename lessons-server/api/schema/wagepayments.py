
from datetime import datetime, timezone, date
from marshmallow import validate, validates, validates_schema, \
    ValidationError, fields

from api import ma
from pytz import utc
from api.auth import token_auth
from models.wagepayment import WagePayment
from models.teacher import Teacher
from api.utils.utils import get_date


class WagePaymentSchema(ma.SQLAlchemySchema):
    class Meta():
        model = WagePayment
        ordered = True

    teacher_id = ma.Integer()
    payment_date = ma.Date(description='Format in utc time')
    start_date = ma.Date(
        required=True,
        description='Format in utc time'
    )
    end_date = ma.Date(
        required=True,
        description='Format in utc time'
    )
    # Dump only
    id = ma.Integer(dump_only=True)
    amount = ma.Float(dump_only=True)
    hours = ma.Float(dump_only=True)
    created_at = ma.DateTime(dump_only=True)
    last_updated = ma.DateTime(dump_only=True)
    referrals_number = ma.Float(dump_only=True)
    referrals_amount = ma.Float(dump_only=True)

    @validates('teacher_id')
    def validate_teacher_id(self, value):
        if Teacher.get_teacher_by_id(value) is None:
            raise ValidationError('Teacher does not exist')

    @validates_schema
    def validate_dates_are_valid(self, data, **kwargs):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if end_date <= start_date:
            raise ValidationError('Dates selected are invalid')
        elif end_date < date(2015, 1, 1) or start_date < date(2015, 1, 1):
            raise ValidationError('Dates selected are invalid')


class CalculateWagePayments(ma.SQLAlchemySchema):
    class Meta:
        model = WagePayment
        ordered = True

    teacher_id = ma.Integer(dump_only=True)
    start_date = ma.Date(required=True, description='Format in utc time')
    end_date = ma.Date(required=True, description='Format in utc time',)
    paid_hours = ma.Float(dump_only=True)
    referrals_number_unpaid = ma.Float(dump_only=True)
    referrals_amount_unpaid = ma.Float(dump_only=True)
    referrals_number_paid = ma.Float(dump_only=True)
    referrals_amount_paid = ma.Float(dump_only=True)
    paid_wage = ma.Float(dump_only=True)
    unpaid_hours = ma.Float(dump_only=True)
    unpaid_wage = ma.Float(dump_only=True)
    referrals_number = ma.Float(dump_only=True)
    referrals_amount = ma.Float(dump_only=True)

    @validates_schema
    def validate_dates_are_valid(self, data, **kwargs):
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        print(type(end_date-start_date))
        if end_date < start_date:
            raise ValidationError('Dates selected are invalid')
        elif end_date < date(2015, 1, 1) or start_date < date(2015, 1, 1):
            raise ValidationError('Dates selected are invalid')


class AddBulkWagePayments(ma.SQLAlchemySchema):
    class Meta:
        model = WagePayment
        ordered = True

    id = ma.Integer(dump_only=True)
    payment_date = ma.DateTime(required=True, validate=[lambda x:x > datetime.now(
        timezone.utc), lambda x:x.tzinfo == timezone.utc])
    start_date = ma.Date(required=True, description='Format in utc time')
    end_date = ma.Date(required=True, description='Format in utc time',)
    amount = ma.Float(dump_only=True)
    hours = ma.Float(dump_only=True)
    referrals_number = ma.Float(dump_only=True)
    referrals_amount = ma.Float(dump_only=True)
    created_at = ma.DateTime(dump_only=True)
    last_updated = ma.DateTime(dump_only=True)

    @validates_schema
    def validate_dates_are_valid(self, data, **kwargs):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if end_date < start_date:
            raise ValidationError('Dates selected are invalid')
        elif end_date < date(2015, 1, 1) or start_date < date(2015, 1, 1):
            raise ValidationError('Dates selected are invalid')
