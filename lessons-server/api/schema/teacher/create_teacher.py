from marshmallow import validate, validates, fields, ValidationError
import phonenumbers
import re

from api import ma
from models.teacher import Teacher
from api.schema.referrals import ReferralSchema
from models.user import User
from api.schema.programs import ProgramsSchema
from api.schema.languages import LanguageSchema
from api.schema.qualifications import QualificationsSchema
from api.schema.subjects import SubjectsSchema
from api.schema.interests import InterestSchema
from api.schema.highschool import HighSchoolSchema
from api.schema.higher_education import HigherEducationProgrammeSchema, HigherEducationInstitutionSchema
from api.schema.user import UserSchema


class CreateTeacherSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Teacher
        ordered = True
    id = ma.Integer(dump_only=True)
    email = fields.String(required=False, validate=[validate.Length(max=120),
                                                    validate.Email()])
    first_name = ma.String(required=False)
    last_name = ma.String(required=False)
    grade_average = ma.Float(required=False)
    bank_number = ma.String()
    reg_number = ma.String()
    how_they_found = ma.String()
    country = ma.String()
    address = ma.String()
    city = ma.String()
    zip_code = ma.String()
    referred_by=ma.String(required=False)
    referral_amount=ma.Float(required=False)
    high_school = fields.List(fields.Nested(
        HighSchoolSchema()), dump_only=True)
    students = fields.List(fields.String, dump_only=True, required=False)
    languages = fields.List(fields.Nested(
        LanguageSchema(),), dump_only=True, required=False)
    referred=ma.String(dump_only=True, required=False)
    referrals=fields.List(fields.Nested(
        ReferralSchema()), dump_only=True)
    qualifications = fields.List(fields.Nested(
        QualificationsSchema()), dump_only=True, required=False)
    subjects = fields.List(fields.Nested(SubjectsSchema()),
                           dump_only=True, required=False)
    programs = fields.List(fields.Nested(ProgramsSchema()), dump_only=True)
    interests = fields.List(fields.Nested(
        InterestSchema()), dump_only=True, required=False)
    status = ma.String(required=False, description='The status of the teacher active/inactive/prospective',
                       validate=validate.OneOf(['active', 'inactive', 'prospective']))
    higher_education_programmes = fields.List(fields.Nested(
        HigherEducationProgrammeSchema()), dump_only=True)
    high_education_institutions = fields.List(fields.Nested(
        HigherEducationInstitutionSchema()), dump_only=True)
    hire_date = ma.DateTime(dump_only=True,)
    wage_per_hour = ma.Float()
    bio = ma.String()
    photo = ma.String()
    phone = ma.String(required=False, validate=[lambda x:x[0] == '+'])
    open_for_new_students = ma.Boolean()
    gender = ma.String(validate=validate.OneOf(['male', 'female']))
    payroll_id = ma.String(required=False)
    higher_education_institution = ma.String(load_only=True, required=False)
    higher_education_programme = ma.String(load_only=True, required=False)
    highschool = ma.String(load_only=True, required=False)
    qualification = ma.String(load_only=True, required=False)
    language = ma.String(load_only=True, required=False)
    interest = ma.String(load_only=True, required=False)
    subjects_create = fields.List(
        fields.String(), load_only=True, required=True)
    programs_create = fields.List(
        fields.String(), load_only=True, required=False)
    finished_highschool = ma.Boolean()
    age = ma.Integer()
    birthday = ma.DateTime()
    updated_on_tw_at = ma.DateTime(dump_only=True)
    created_on_tw_at = ma.DateTime(dump_only=True)
    created_at= ma.DateTime(dump_only=True)
    last_updated= ma.DateTime(dump_only=True)
    @validates('email')
    def validate_teacher_email(self, value):
        if User.find_by_email(value) is not None:
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
