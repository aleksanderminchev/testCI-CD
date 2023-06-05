import re
import phonenumbers

from marshmallow import validate, validates, ValidationError, fields
from api.schema.teacher.teachers import TeacherSchema
from api.schema.student import StudentSchema
from api.schema.customers import CustomerSchema
from api import ma
from models.user import User
from api.auth import token_auth


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        ordered = True

    uid = ma.auto_field(dump_only=True)
    email = ma.auto_field(
        required=True,
        validate=[validate.Length(max=120),
                  validate.Email()]
    )
    password = ma.String(required=True, load_only=True,
                         validate=validate.Length(min=3))
    roles = fields.List(fields.String(), dump_only=True)
    admin = ma.Boolean(dump_only=True)
    student = ma.Boolean(dump_only=True)
    student_dict = fields.Nested(StudentSchema, dump_only=True)
    teacher = ma.Boolean(dump_only=True)
    teacher_dict = fields.Nested(TeacherSchema, dump_only=True)
    customer = ma.Boolean(dump_only=True)
    customer_dict = fields.Nested(CustomerSchema, dump_only=True)
    first_name = ma.String(required=False, validate=[
                           validate.Length(max=120, min=2)])
    last_name = ma.String(required=False, validate=[
        validate.Length(max=120, min=2)])
    phone = ma.String(required=False, validate=[
                      validate.Regexp('^\+\d{6,16}$')])
    created_at = ma.DateTime(dump_only=True)
    last_updated = ma.DateTime(dump_only=True)
    last_login = ma.DateTime(dump_only=True)
    is_verified = ma.Boolean(dump_only=True)

    @ validates('email')
    def validate_email(self, value):
        user = token_auth.current_user()
        old_email = user.email if user else None
        if value != old_email and \
                User.find_by_email(email=value):
            raise ValidationError('Email already exists.')

    @ validates('phone')
    def validate_phone(self, value):
        value = value.replace(" ", "")
        if re.match(r'^\+\d{1,4}\d{4,14}$', value):
            phone_number = phonenumbers.parse(value)
            if not phonenumbers.is_valid_number(phone_number):
                raise ValidationError('Phone number is not valid')
        else:
            raise ValidationError('Invalid phone number length')


class UpdateUserSchema(UserSchema):
    old_password = ma.String(load_only=True, validate=validate.Length(min=3))

    @ validates('old_password')
    def validate_old_password(self, value):
        if not token_auth.current_user().verify_password(value):
            raise ValidationError('Password is incorrect')
