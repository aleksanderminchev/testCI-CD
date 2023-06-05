
from datetime import datetime, timezone
from marshmallow import validate, validates, validates_schema, \
    ValidationError, fields

from api import ma
from pytz import utc 
from api.auth import token_auth
from models.balance import Balance
from api.utils.utils import get_date
from api.schema.transactions import TransactionSchema
from api.schemas import OrderSchema


class BalanceSchema(ma.SQLAlchemySchema):
    class Meta():
        model=Balance
        ordered=True
    id=ma.Integer(dump_only=True)
    customer_id=ma.Integer(required=True)
    hours_used=ma.Float(dump_only=True)
    hours_scheduled=ma.Float(dump_only=True)
    hours_ordered=ma.Float(dump_only=True)
    hours_free=ma.Float(dump_only=True)
    invoice_balance=ma.Float(dump_only=True)
    current_balance=ma.String(dump_only=True)
    transactions=fields.List(fields.Nested(TransactionSchema()), dump_only=True)
    orders=fields.List(fields.Nested(OrderSchema()), dump_only=True)
class RevenueAccountingSchema(ma.SQLAlchemySchema):
    class Meta:
        ordered=True
    start_date=ma.Date(load_only=True)
    end_date=ma.Date(load_only=True)
class AccountingBalanceSchema(ma.SQLAlchemySchema):
    class Meta:
        ordered=True
    date=ma.Date(load_only=True)
    id=ma.Integer(dump_only=True)
    customer_name=ma.String(dump_only=True)
    email=ma.String(dump_only=True)
    net_payments=ma.Float(dump_only=True)
    balance=ma.Float(dump_only=True)
    prepayments=ma.String(dump_only=True)
    receivables=ma.String(dump_only=True)
    total_bookings_value=ma.Float(dump_only=True)
class AddOrderToBalanceSchema(BalanceSchema):
    class Meta():
        model=Balance
        ordered=True
    order_id=ma.String(required=True)

class AddTransactionToBalanceSchema(BalanceSchema):
    class Meta():
        model=Balance
        ordered=True
    transaction_id=ma.Integer(required=True)
class RecalculateBalanceSchema(ma.SQLAlchemySchema):
    class Meta():
        model=Balance
        ordered=True
    lesson_id=ma.Integer(required=True)

class UseLessonSchema(BalanceSchema):
    class Meta():
        model=Balance
        ordered=True
    lesson_id=ma.Integer(required=True)