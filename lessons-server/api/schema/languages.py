from marshmallow import validate, validates, validates_schema, \
    ValidationError, fields

from api import ma
from api.auth import token_auth
from models.language import Language,User
from models.teacher import Teacher

class LanguageSchema(ma.SQLAlchemySchema):
    class Meta:
        model= Language
        ordered = True
    id=ma.Integer(dump_only=True)
    name=ma.String(required=True)


class UpdateLanguagesSchema(LanguageSchema):
    class Meta:
        model= Language
        ordered = True
    id=ma.Integer(required=True)
    name=ma.String(required=True)
    @validates("id")
    def validate_language_id(self,value):
       if Language.get_language_by_id(value) is None:
           raise ValidationError("No language was found")
class AddLanguageToTeacher(ma.SQLAlchemySchema):
    class Meta:
        model=Teacher
        ordered=True
    
    language_id=fields.List(fields.Integer(),required=True,load_only=True)
    teacher_email=ma.String(required=True,load_only=True)
    id=ma.String(dump_only=True)
    name=ma.String(dump_only=True)
    @validates('language_id')
    def validate_student_id(self,value):
        if Language.get_language_by_id(value) is None:
            raise ValidationError('No subject was found')
    @validates('teacher_email')
    def validate_teacher_email(self,value):
        if User.find_by_email(value) is None:
            raise ValidationError('No email was found')
        elif User.find_by_email(value).teacher is None:
            raise ValidationError('No teacher was found with this email was found')
