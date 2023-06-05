
from datetime import datetime, timezone
from marshmallow import validate, validates, validates_schema, \
    ValidationError, fields

from api import ma
from pytz import utc 
from api.auth import token_auth
from models.higher_education_institution import HigherEducationInstitution
from models.higher_education_programme import HigherEducationProgramme
from models.user import User
class HigherEducationInstitutionSchema(ma.SQLAlchemySchema):
    class Meta():
        model=HigherEducationInstitution
        ordered=True
    id=ma.Integer()
    name=ma.String(dump_only=True)

class HigherEducationProgrammeSchema(ma.SQLAlchemySchema):
    class Meta():
        model=HigherEducationProgramme
        ordered=True
    id=ma.Integer()
    name=ma.String(dump_only=True)

class AttachHigherEduInstitution(HigherEducationInstitutionSchema):
    class Meta():
        model=HigherEducationInstitution
        ordered=True
    teacher_email=ma.String()
    @validates('id')
    def validate_student_id(self,value):
        if HigherEducationInstitution.query.get(value) is None:
            raise ValidationError('No higher education was found')
    @validates('teacher_email')
    def validate_teacher_email(self,value):
        if User.find_by_email(value) is None:
            raise ValidationError('No email was found')
        elif User.find_by_email(value).teacher is None:
            raise ValidationError('No teacher was found with this email was found')

class AttachHigherEduProgramme(HigherEducationProgrammeSchema):
    class Meta():
        model=HigherEducationProgramme
        ordered=True
    teacher_email=ma.String()
    @validates('id')
    def validate_student_id(self,value):
        if HigherEducationProgramme.query.get(value) is None:
            raise ValidationError('No higher education was found')
    @validates('teacher_email')
    def validate_teacher_email(self,value):
        if User.find_by_email(value) is None:
            raise ValidationError('No email was found')
        elif User.find_by_email(value).teacher is None:
            raise ValidationError('No teacher was found with this email was found')
