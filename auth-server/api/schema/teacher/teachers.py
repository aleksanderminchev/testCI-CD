from marshmallow import validate, validates, validates_schema, \
    ValidationError, fields
import phonenumbers
import re
from api import ma
from api.auth import token_auth
from models.teacher import Teacher
from api.schema.referrals import ReferralSchema
from models.student import Student
from api.schema.programs import ProgramsSchema
from api.schema.languages import LanguageSchema
from api.schema.qualifications import QualificationsSchema
from api.schema.subjects import SubjectsSchema
from api.schema.interests import InterestSchema
from models.student import Student
from models.user import User
from api.schema.highschool import HighSchoolSchema
from api.schema.higher_education import HigherEducationProgrammeSchema, HigherEducationInstitutionSchema
# Teacher Schemas

# subject_list=fields.List(fields.String(required=True))


class TeacherSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Teacher
        ordered = True
    id = ma.Integer(dump_only=True)
    email = fields.String(required=False)
    first_name = ma.String(dump_only=True)
    last_name = ma.String(dump_only=True)
    students = fields.List(fields.String, dump_only=True, required=False)
    languages = fields.List(fields.Nested(
        LanguageSchema(),), dump_only=True, required=False)
    qualifications = fields.List(fields.Nested(
        QualificationsSchema()), dump_only=True, required=False)
    subjects = fields.List(fields.Nested(SubjectsSchema()),
                           dump_only=True, required=False)
    interests = fields.List(fields.Nested(
        InterestSchema()), dump_only=True, required=False)
    hire_date = ma.DateTime(dump_only=True,)
    wage_per_hour = ma.Float(dump_only=True)
    bank_number = ma.String(dump_only=True)
    reg_number = ma.String(dump_only=True)
    how_they_found = ma.String(dump_only=True)
    country = ma.String(dump_only=True)
    address = ma.String(dump_only=True)
    city = ma.String(dump_only=True)
    zip_code = ma.String(dump_only=True)
    bio = ma.String(dump_only=True,)
    photo = ma.String(dump_only=True)
    phone = ma.String()
    open_for_new_students = ma.Boolean(dump_only=True)
    gender = ma.String(
        dump_only=True, validate=validate.OneOf(['male', 'female']))
    status = ma.String(dump_only=True, required=False, description='The status of the teacher active/inactive/prospective',
                       validate=validate.OneOf(['active', 'inactive', 'prospective']))
    programs = fields.List(fields.Nested(ProgramsSchema()), dump_only=True)
    grade_average = ma.Float(dump_only=True)
    payroll_id = ma.String(dump_only=True, required=False)
    referred=ma.String(dump_only=True, required=False)
    referrals=fields.List(fields.Nested(
        ReferralSchema()), dump_only=True)
    higher_education_programmes = fields.List(fields.Nested(
        HigherEducationProgrammeSchema()), dump_only=True)
    higher_education_institutions = fields.List(fields.Nested(
        HigherEducationInstitutionSchema()), dump_only=True)
    high_school = fields.List(fields.Nested(
        HighSchoolSchema()), dump_only=True)
    finished_highschool = ma.Boolean(dump_only=True)
    age = ma.Integer(dump_only=True)
    birthday = ma.DateTime(dump_only=True)
    updated_on_tw_at = ma.DateTime(dump_only=True)
    created_on_tw_at = ma.DateTime(dump_only=True)
    created_at= ma.DateTime(dump_only=True)
    last_updated= ma.DateTime(dump_only=True)

class FilterTeacherShema(TeacherSchema):
    class Meta:
        model = Teacher
        ordered = True
    age = ma.Integer(required=False)
    gender = ma.String(validate=validate.OneOf(['male', 'female']))

    first_name = ma.String(
        required=False, description='Put the field name here')
    last_name = ma.String(
        required=False, description='Put the filter value here')
    wage_per_hour = ma.Float(
        required=False, description='Wage of teacher per hour')
    bank_number = ma.String()
    reg_number = ma.String()
    how_they_found = ma.String()
    country = ma.String()
    address = ma.String()
    city = ma.String()
    zip_code = ma.String()
    hire_date = ma.Date(required=False,)
    status = ma.String(required=False, description='The status of the teacher active/inactive/prospective',
                       validate=validate.OneOf(['active', 'inactive', 'prospective']))
    id = ma.Integer(dump_only=True)
    bio = ma.String(required=False, description='', dump_only=True)
    photo = ma.String(required=False, description='', dump_only=True)
    open_for_new_students = ma.Boolean(required=False, description='',)
    high_school = ma.String(required=False, description='', )
    birthday = ma.DateTime(required=False, description='',)
    finished_highschool = ma.Boolean(required=False, description='',)
    higher_education_institution = ma.Integer(required=False, description='',)
    higher_education_programme = ma.Integer(required=False, description='',)
    language = ma.Integer(required=False, description='',)
    qualification = ma.Integer(required=False, description='',)
    interest = ma.Integer(required=False, description='',)
    subject = ma.Integer(required=False, description='',)
    program = ma.Integer(required=False, description='',)
    updated_on_tw_at = ma.DateTime(dump_only=True)
    created_on_tw_at = ma.DateTime(dump_only=True)
    created_at= ma.DateTime(dump_only=True)
    last_updated= ma.DateTime(dump_only=True)

class AddStudentToTeacher(ma.SQLAlchemySchema):
    class Meta:
        model = Teacher
        ordered = True

    # Required:
    student_id = fields.List(fields.Integer(required=True),required=True)
    teacher_email = ma.String(required=True)

    # Dump only:
    email = ma.String(dump_only=True)
    admin = ma.Boolean(dump_only=True)
    first_name = ma.String(dump_only=True)
    last_name = ma.String(dump_only=True)
    phone = ma.String(dump_only=True)
    created_at = ma.DateTime(dump_only=True)
    last_updated = ma.DateTime(dump_only=True)
    last_login = ma.DateTime(dump_only=True)
    customer_id=ma.String(dump_only=True)
    created_at= ma.DateTime(dump_only=True)
    last_updated= ma.DateTime(dump_only=True)
    @validates('student_id')
    def validate_student_id(self, value):
        for i in value:
            if Student.get_student_by_id(i) is None:
                raise ValidationError('No student was found')

    @validates('teacher_email')
    def validate_teacher_email(self, value):
        if User.find_by_email(value) is None:
            raise ValidationError('No email was found')
        elif User.find_by_email(value).teacher is None:
            raise ValidationError(
                'No teacher was found with this email was found')


class UpdateTeacherSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Teacher
        ordered = True
    id = ma.Integer(
        required=True, description="Teacher Id with which to update", validate=[])
    first_name = ma.String(
        required=False, description='Put the first_name here')
    last_name = ma.String(required=False, description='Put the last_name here')
    phone = ma.String()
    email = ma.String(required=False, description='Email',validate=validate.Email())
    languages = fields.List(fields.Nested(
        LanguageSchema(),), dump_only=True, required=False)
    qualifications = fields.List(fields.Nested(
        QualificationsSchema()), dump_only=True, required=False)
    subjects = fields.List(fields.Nested(SubjectsSchema()),
                           dump_only=True, required=False)
    interests = fields.List(fields.Nested(
        InterestSchema()), dump_only=True, required=False)
    programs = fields.List(fields.Nested(ProgramsSchema()), dump_only=True)
    higher_education_programmes = fields.List(fields.Nested(
        HigherEducationProgrammeSchema()), dump_only=True)
    referred=ma.String(dump_only=True, required=False)
    referrals=fields.List(fields.Nested(
        ReferralSchema()), dump_only=True)
    higher_education_institutions = fields.List(fields.Nested(
        HigherEducationInstitutionSchema()), dump_only=True)
    high_school = fields.List(fields.Nested(
        HighSchoolSchema()), dump_only=True)
    students = fields.List(fields.String, dump_only=True, required=False)
    hire_date = ma.DateTime(dump_only=True,)
    bank_number = ma.String()
    reg_number = ma.String()
    how_they_found = ma.String()
    country = ma.String()
    address = ma.String()
    city = ma.String()
    zip_code = ma.String()
    status = ma.String(required=False, description='The status of the teacher active/inactive/prospective',
                       validate=validate.OneOf(['active', 'inactive', 'prospective']))
    grade_average = ma.Float()
    wage_per_hour = ma.Float(required=False)
    bio = ma.String()
    photo = ma.String()
    open_for_new_students = ma.Boolean()
    gender = ma.String(validate=validate.OneOf(['male', 'female']))
    payroll_id = ma.String(required=False)
    higher_education_institutions_update = fields.List(
        fields.Integer(), required=False, load_only=True)
    higher_education_programmes_update = fields.List(
        fields.Integer(), required=False, load_only=True)
    qualifications_update = fields.List(
        fields.Integer(), required=False, load_only=True)
    subjects_update = fields.List(
        fields.Integer(), required=False, load_only=True)
    languages_update = fields.List(
        fields.Integer(), required=False, load_only=True)
    interests_update = fields.List(
        fields.Integer(), required=False, load_only=True)
    high_school_update = fields.List(
        fields.Integer(), required=False, load_only=True)
    programs_update = fields.List(
        fields.Integer(), required=False, load_only=True)
    finished_highschool = ma.Boolean()
    age = ma.Integer()
    birthday = ma.DateTime()
    created_at= ma.DateTime(dump_only=True)
    last_updated= ma.DateTime(dump_only=True)
    updated_on_tw_at = ma.DateTime(dump_only=True)
    created_on_tw_at = ma.DateTime(dump_only=True)

    @validates_schema
    def validate_teacher_email(self, data, **kwargs):
        email = data.get('email') or None
        id = data.get('id')
        teacher = Teacher.query.get(id)
        if teacher is None:
            raise ValidationError("Error with identifying the teacher")
        if email is not None:
            email_user = User.find_by_email(email)
            if email_user is not None:
                print(email_user)
                if teacher.user is not email_user:
                    raise ValidationError('Email is used')

    @validates('phone')
    def validate_phone(self, value):
        phone = value or None
        print(phone)
        if phone is not None:
            phone = phone.replace(" ", "")
            if phone[0] != '+':
                raise ValidationError(
                    'Phone number is not valid. Must include country code.')
            elif re.match(r'^\+\d{1,4}\d{4,14}$', phone):
                phone_number = phonenumbers.parse(phone)
                if not phonenumbers.is_valid_number(phone_number):
                    raise ValidationError('Phone number is not valid')
            else:
                raise ValidationError('Invalid phone number length')


class CalendarTeacher(ma.Schema):

    class Meta:
        ordered = True
        model = Teacher
    filter_status = ma.String(load_only=True)
    students = fields.List(fields.Integer(), dump_only=True)
    first_name = ma.String(dump_only=True)
    last_name = ma.String(dump_only=True)
    email = ma.String(dump_only=True)
    id = ma.Integer(dump_only=True)
    status = ma.String(dump_only=True)
    