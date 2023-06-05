import re
import phonenumbers

from datetime import datetime, timezone

from numpy import require
from marshmallow import validate, validates, validates_schema, \
    ValidationError, fields
from api import ma
from pytz import utc
from api.auth import token_auth
from models.user import User
from models.customer import Customer
from models.student import Student
# Customer Schemas


class CustomerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        ordered = True

    id = ma.Integer(dump_only=True)
    email = ma.auto_field(required=True, validate=[validate.Length(max=120),
                                                   validate.Email()])

    first_name = ma.String(required=False)
    last_name = ma.String(required=False)
    students = fields.List(fields.String, dump_only=True, required=False)
    phone = ma.String(required=False, validate=[lambda x:x[0] == '+'])
    email_lesson_reminders = ma.Boolean(dump_only=True)
    email_lesson_notes = ma.Boolean(dump_only=True)
    status = ma.String(dump_only=True)
    customer_type = ma.String(dump_only=True)
    created_at = ma.DateTime(dump_only=True)
    last_updated = ma.DateTime(dump_only=True)

    @validates('email')
    def validate_email(self, value):
        user = token_auth.current_user()
        old_email = user.email if user else None
        if value != old_email and \
                User.query.filter_by(email=value).first():
            raise ValidationError('Use a different email.')

    @validates('phone')
    def validate_phone(self, value):
        value = value.replace(" ", "")
        if re.match(r'^\+\d{1,4}\d{4,14}$', value):
            phone_number = phonenumbers.parse(value)
            if not phonenumbers.is_valid_number(phone_number):
                raise ValidationError('Phone number is not valid')
        else:
            raise ValidationError('Invalid phone number length')


class UpdateCustomerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Customer
        ordered = True

    # Options to update
    id = ma.Integer(required=True, description="Customer Id")

    email = ma.Email(
        required=False,
        validate=[validate.Length(max=120), validate.Email()]
    )

    first_name = ma.String(required=False)
    last_name = ma.String(required=False)
    phone = ma.String(required=False, validate=[lambda x:x[0] == '+'])
    email_lesson_reminder = ma.Boolean(required=False)
    email_lesson_notes = ma.Boolean(required=False)
    stripe_id = ma.String(required=False)

    # Dump Only
    status = ma.String(dump_only=True)
    customer_type = ma.String(
        dump_only=True,
        validate=validate.OneOf(["independent", "family"])
    )
    created_at = ma.DateTime(dump_only=True)
    last_updated = ma.DateTime(dump_only=True)

    @validates('id')
    def validate_customer_existence(self, value):
        customer = Customer.get_customer_by_id(value)
        if customer is None:
            raise ValidationError("Customer ID not found.")

    @validates('phone')
    def validate_phone(self, value):
        value = value.replace(" ", "")
        if re.match(r'^\+\d{1,4}\d{4,14}$', value):
            phone_number = phonenumbers.parse(value)
            if not phonenumbers.is_valid_number(phone_number):
                raise ValidationError('Phone number is not valid')
        else:
            raise ValidationError('Invalid phone number length')


class StudentIndependToFamily(CustomerSchema):
    class Meta:
        model = User
        ordered = True

    old_email = ma.String(required=True, load_only=True)
    gender = ma.String(dump_only=True)
    email_lesson_reminders = ma.Boolean(dump_only=True)
    email_lesson_notes = ma.Boolean(dump_only=True)
    status = ma.String(dump_only=True)
    student_type = ma.String(dump_only=True)

    @validates('email')
    def validate_student_email_is_not_null(self, value):
        if Student.query.filter_by(email=value).first():
            raise ValidationError('Invalid email address')

    @validates('old_email')
    def validate_old_email(self, value):
        user = token_auth.current_user()
        old_email = user.email if user else None
        if User.query.filter_by(email=value).first() is None:
            raise ValidationError('Use a different email.')


class AddStudentToFamilySchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        ordered = True
    email = ma.auto_field(required=True, validate=[validate.Length(max=120),
                                                   validate.Email()])
    first_name = ma.String(required=True)
    last_name = ma.String(required=True)
    gender = ma.String(
        required=True, validate=validate.OneOf(['male', 'female']))
    email_lesson_reminders = ma.Boolean(dump_only=True)
    email_notes_reminders = ma.Boolean(dump_only=True)
    status = ma.String(dump_only=True)
    student_type = ma.String(dump_only=True)
    created_at = ma.DateTime(dump_only=True)
    last_updated = ma.DateTime(dump_only=True)
    student_added = ma.Boolean(dump_only=True)

    @validates('email')
    def validate_email(self, value):
        user = token_auth.current_user()
        old_email = user.email if user else None
        user_object = User.query.filter_by(email=value).first()
        if user_object is None:
            raise ValidationError('Use a different email.')
        elif user_object.customer.customer_type.value == 'independent':
            raise ValidationError(
                'A non-family account is trying to add a student')


class AddFamilyWithStudent(ma.SQLAlchemySchema):
    class Meta:
        model = User,
        ordered = True
    email = ma.String(required=True, validate=[validate.Length(max=120),
                                               validate.Email()])
    student_first_name = ma.String(required=True)
    student_last_name = ma.String(required=True)
    first_name = ma.String(required=True)
    last_name = ma.String(required=True)
    phone = ma.String(required=True, validate=[lambda x: x[0] == '+'])
    gender = ma.String(
        required=True, validate=validate.OneOf(['male', 'female']))
    email_lesson_reminders = ma.Boolean(dump_only=True)
    email_notes_reminders = ma.Boolean(dump_only=True)
    status = ma.String(dump_only=True)
    student_type = ma.String(dump_only=True)
    created_at = ma.DateTime(dump_only=True)
    last_updated = ma.DateTime(dump_only=True)
    student_added = ma.Boolean(dump_only=True)

    @validates('email')
    def validate_email(self, value):
        user = token_auth.current_user()
        user_object = User.query.filter_by(email=value).first()
        if user_object is not None:
            raise ValidationError('Use a different email.')

    @validates('phone')
    def validate_phone(self, value):
        value = value.replace(" ", "")
        if re.match(r'^\+\d{1,4}\d{4,14}$', value):
            phone_number = phonenumbers.parse(value)
            if not phonenumbers.is_valid_number(phone_number):
                raise ValidationError('Phone number is not valid')
        else:
            raise ValidationError('Invalid phone number length')


class ChangeStatusSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        ordered = True
    uid = ma.auto_field(dump_only=True,)
    email = ma.Email(required=True, validate=[validate.Length(max=120),
                                              validate.Email()])
    status = ma.String(
        required=True, validate=validate.OneOf(["active", "inactive"]))
    created_at = ma.DateTime(dump_only=True)
    last_updated = ma.DateTime(dump_only=True)
    first_name = ma.String(dump_only=True)
    last_name = ma.String(dump_only=True)
    phone = ma.String(dump_only=True)
    created_at = ma.DateTime(dump_only=True)
    last_updated = ma.DateTime(dump_only=True)

    @validates('email')
    def validate_email(self, value):
        user = token_auth.current_user()
        old_email = user.email if user else None
        if User.query.filter_by(email=value).first() is None:
            raise ValidationError('Use a different email.')

    @validates('email')
    def validate_email_is_customers(self, value):
        if len(User.query.filter_by(email=value).first().customer) == 0:
            raise ValidationError('This email is not a valid customer')
