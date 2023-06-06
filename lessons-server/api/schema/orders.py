from models.order import Order
from datetime import datetime, timezone
from marshmallow import validate, validates, validates_schema, \
    ValidationError, fields

from api import ma


class VoidOrderSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Order
        ordered = True
    id = ma.Integer(required=True)

    @validates('id')
    def validate_user(self, value):
        order = Order.get_order_by_id(id=value)
        if order is None:
            raise ValidationError('Invalid Order')
        elif order.balance is None:
            raise ValidationError('Invalid Balance')
        elif order.status.value == 'void':
            raise ValidationError('Voiding a voided order already')
