import phonenumbers
import re

from marshmallow import validate, validates, validates_schema, \
    ValidationError, fields

from api import ma
from api.auth import token_auth
from models.user import User
from models.teacher import Teacher, Student
from models.customer import Customer

# Student Schemas


class CreateStudentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Student
        ordered = True

    id = ma.Integer(required=True)
    email = ma.Email(required=True, description='Email address for the student', validate=[validate.Length(max=120),
                                                                                           validate.Email()])
    gender = ma.String(required=True, description="The gender of the student",
                       validate=validate.OneOf(["male", "female"]))
    first_name = ma.String(required=True)
    last_name = ma.String(required=True)
    email_lesson_reminders = ma.Boolean(dump_only=True)
    email_lesson_notes = ma.Boolean(dump_only=True)
    status = ma.String(dump_only=True, validate=validate.OneOf(
        ["active", "inactive"]))
    student_type = ma.String(
        dump_only=True, validate=validate.OneOf(["independent", "child"]))
    phone = ma.String(
        required=True, description="The phone number of the student. Must include country code.",)
    teachers = fields.List(fields.String, dump_only=True, required=False)
    # subject_list=fields.List(fields.String(required=True))
    customer_id = ma.String(dump_only=True)

    @validates('id')
    def validate_id(self, value):
        if Customer.query.get(value) is None:
            raise ValidationError("Error itentifying the customer")

    @validates('email')
    def validate_account_existence(self, value):
        query_user = User.query.filter_by(email=value).first()
        query_student = Student.query.filter_by(email=value).first()
        if query_user is not None or query_student is not None:
            raise ValidationError("Error identifying the email")

    @validates('email')
    def validate_account_type(self, value):
        query_user = User.query.filter_by(email=value).first()
        # if query_user.customer.customer_type.value =='independent':
        #    raise ValidationError('A non-family account is trying to add a student')


class CreateStudentYoungSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Student
        ordered = True

    id = ma.Integer(required=True)
    email = ma.Email(required=True, description='Email address for the student', validate=[validate.Length(max=120),
                                                                                           validate.Email()])
    gender = ma.String(required=True, description="The gender of the student",
                       validate=validate.OneOf(["male", "female"]))
    email_lesson_reminders = ma.Boolean(dump_only=True)
    email_lesson_notes = ma.Boolean(dump_only=True)
    status = ma.String(dump_only=True, validate=validate.OneOf(
        ["active", "inactive"]))
    student_type = ma.String(dump_only=True, validate=validate.OneOf(
        ["independent", "child"]))
    first_name = ma.String(required=True)
    last_name = ma.String(required=True)
    phone = ma.String(dump_only=True)
    teachers = fields.List(fields.String, dump_only=True, required=False)
    customer_id = ma.String(dump_only=True)
    # subject_list=fields.List(fields.String(required=True))

    @validates('id')
    def validate_id(self, value):
        if Customer.query.get(value) is None:
            raise ValidationError("Error itentifying the customer")

    @validates('email')
    def validate_account_existence(self, value):
        query_user = User.query.filter_by(email=value).first()
        query_student = Student.query.filter_by(email=value).first()
        if query_user is not None or query_student is not None:
            raise ValidationError("Error identifying the email")

    @validates('email')
    def validate_account_type(self, value):
        query_user = User.query.filter_by(email=value).first()


class StudentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Student
        ordered = True
    # Required fields:
    email = ma.Email(required=True, validate=[validate.Length(max=120),
                                              validate.Email()])
    gender = ma.String(required=True, description="The gender of the student",
                       validate=validate.OneOf(["male", "female"]))
    first_name = ma.String(required=True)
    last_name = ma.String(required=True)
    status = ma.String(required=True, validate=validate.OneOf(
        ["active", "inactive"]))

    # Dump_only
    id = ma.Integer(dump_only=True)
    phone = ma.String(dump_only=True)
    email_lesson_reminders = ma.Boolean(dump_only=True)
    created_at = ma.Date(dump_only=True)
    last_updated_at = ma.Date(dump_only=True)
    email_lesson_notes = ma.Boolean(dump_only=True)
    customer_id = ma.String(dump_only=True)
    status = ma.String(dump_only=True, validate=validate.OneOf(
        ["active", "inactive"]))
    student_type = ma.String(dump_only=True, validate=validate.OneOf(
        ["child", "independent"]))
    teachers = fields.List(fields.String, dump_only=True, required=False)

    @validates('email')
    def validate_account_existence(self, value):
        query_user = User.find_by_email(email=value)
        if query_user is None:
            raise ValidationError("Wrong email provided")


class UpdateStudentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Student
        ordered = True
    # Required
    id = ma.Integer(required=True, description="Student Id")

    # Optional
    email = ma.Email(
        required=True,
        validate=[validate.Length(max=120), validate.Email()]
    )
    first_name = ma.String(required=False)
    last_name = ma.String(required=False)
    email_lesson_reminders = ma.Boolean(required=False)
    email_lesson_notes = ma.Boolean(required=False)
    phone = ma.String(required=False, validate=[lambda x:x[0] == '+'])
    gender = ma.String(
        required=False,
        description="The gender of the student",
        validate=validate.OneOf(["male", "female"])
    )

    # Dump only
    status = ma.String(
        dump_only=True,
        validate=validate.OneOf(["active", "inactive"])
    )
    customer_id = ma.String(dump_only=True)
    student_type = ma.String(dump_only=True, validate=validate.OneOf(
        ["independent", "child"]))
    created_at = ma.DateTime(dump_only=True)
    last_updated = ma.DateTime(dump_only=True)
    teachers = fields.List(fields.String, dump_only=True, required=False)
    # subject_list=fields.List(fields.String(required=True))

    @validates_schema
    def validate_student_email(self, data, **kwargs):
        email = data.get('email') or None
        id = data.get('id')
        student = Student.query.get(id)
        if student is None:
            raise ValidationError("Error with identifying the student")
        if email is not None and student.student_type.value == 'independent':
            email_user = User.find_by_email(email)
            if email_user is not None:
                if student.user is not email_user:
                    raise ValidationError('Email is used')

    @validates('phone')
    def validate_phone(self, value):
        value = value.replace(" ", "")
        if re.match(r'^\+\d{1,4}\d{4,14}$', value):
            phone_number = phonenumbers.parse(value)
            if not phonenumbers.is_valid_number(phone_number):
                raise ValidationError('Phone number is not valid')
        else:
            raise ValidationError('Invalid phone number length')


class GetLessonSpace(ma.SQLAlchemySchema):
    class Meta:
        model = Student
        ordered = True

    url = ma.String(dump_only=True, required=True)


class AddTeacherToStudent(ma.SQLAlchemySchema):
    class Meta:
        model = Student
        ordered = True

    # Required:
    teacher_id = fields.List(fields.Integer(
        load_only=True, required=True), required=True)
    student_email = ma.String(required=True)

    # Dump only:
    email = ma.String(dump_only=True)
    admin = ma.Boolean(dump_only=True)
    first_name = ma.String(dump_only=True)
    last_name = ma.String(dump_only=True)
    phone = ma.String(dump_only=True)
    created_at = ma.DateTime(dump_only=True)
    last_updated = ma.DateTime(dump_only=True)
    last_login = ma.DateTime(dump_only=True)

    @validates('teacher_id')
    def validate_student_id(self, value):
        for i in value:
            if Teacher.get_teacher_by_id(i) is None:
                raise ValidationError('No teacher was found')

    @validates('student_email')
    def validate_teacher_email(self, value):
        if Student.query.filter_by(email=value).first() is None:
            raise ValidationError('No email was found')
