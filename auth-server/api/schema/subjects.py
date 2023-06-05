from marshmallow import validate, validates, validates_schema, \
    ValidationError, fields

from api import ma
from api.auth import token_auth
from models.user import User
from models.teacher import Teacher
from models.subjects import Subjects


class SubjectsSchema(ma.SQLAlchemySchema):
    class Meta:
        model= Subjects
        ordered = True
    id=ma.Integer(dump_only=True)
    name=ma.String(required=True)


class UpdateSubjectsSchema(SubjectsSchema):
    class Meta:
        model= Subjects
        ordered = True
    id=ma.Integer(required=True)
    name=ma.String(required=True)
    @validates("id")
    def validate_subject_id(self,value):
       if Subjects.get_subject_by_id(value) is None:
           raise ValidationError("No subject was found")
class AddSubjectToTeacher(ma.SQLAlchemySchema):
    class Meta:
        model=Teacher
        ordered=True
    
    subject_id=fields.List(fields.Integer(),load_only=True,required=True)
    teacher_email=ma.String(load_only=True,required=True)
    id=ma.String(dump_only=True)
    name=ma.String(dump_only=True)
    @validates('subject_id')
    def validate_student_id(self,value):
        if Subjects.query.get(value) is None:
            raise ValidationError('No subject was found')
    @validates('teacher_email')
    def validate_teacher_email(self,value):
        if User.find_by_email(value) is None:
            raise ValidationError('No email was found')
        elif User.find_by_email(value).teacher is None:
            raise ValidationError('No teacher was found with this email was found')