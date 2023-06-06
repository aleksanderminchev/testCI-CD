
from datetime import datetime, timezone
from marshmallow import validate, validates, validates_schema, \
    ValidationError, fields

from api import ma
from pytz import utc
from api.auth import token_auth
from models.transaction import Transaction
from api.schema.customers import CustomerSchema, Customer
from api.utils.utils import get_date


class TransactionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Transaction
        ordered = True
    id = ma.Integer()
    type_transaction = ma.String()
    created_at = ma.DateTime(dump_only=True)
    last_updated = ma.DateTime(dump_only=True)
    currency = ma.String(dump_only=True)
    amount = ma.Float(dump_only=True)
    void = ma.Boolean(dump_only=True)
    method = ma.String(dump_only=True)
    stripe_transaction_id = ma.String(dump_only=True)
    customer = fields.Nested(CustomerSchema, dump_only=True)


class CreateTransactionSchema(ma.SQLAlchemySchema):
    customer_id = ma.Integer(required=True)
    type_transaction = ma.String(
        required=True, validate=validate.OneOf(['payment', 'refund']))
    created_at = ma.DateTime(dump_only=True)
    last_updated = ma.DateTime(dump_only=True)
    currency = ma.String(required=True, validate=validate.OneOf(['DKK']))
    amount = ma.Float(required=True)
    void = ma.Boolean(required=True)
    method = ma.String(required=True, validate=validate.OneOf(
        ['bank', 'stripe', 'other']))
    stripe_transaction_id = ma.String()
    customer = fields.Nested(CustomerSchema, dump_only=True)

    @validates('customer_id')
    def validate_customer_id(self, value):
        if Customer.get_customer_by_id(value) is None:
            raise ValidationError('Customer not found')


class UpdateTransactionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Transaction
        ordered = True
    id = ma.Integer(required=True)
    type_transaction = ma.String(
        required=True, validate=validate.OneOf(['payment', 'refund']))
    created_at = ma.DateTime(dump_only=True)
    last_updated = ma.DateTime(dump_only=True)
    currency = ma.String(required=True, validate=validate.OneOf(['DKK']))
    amount = ma.Float(required=True)
    void = ma.Boolean(required=True)
    method = ma.String(required=True, validate=validate.OneOf(
        ['bank', 'stripe', 'other']))
    stripe_transaction_id = ma.String()
    customer = fields.Nested(CustomerSchema, dump_only=True)

    @validates('id')
    def validate_customer_id(self, value):
        if Transaction.get_transaction_by_id(value) is None:
            raise ValidationError('Transaction not found')
