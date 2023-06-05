from marshmallow import validate, validates, validates_schema, \
    ValidationError, fields

from api import ma
from api.auth import token_auth
from models.user import User
from models.teacher import Teacher
from models.interest import Interest


class InterestSchema(ma.SQLAlchemySchema):
    class Meta:
        model= Interest
        ordered = True
    id=ma.Integer(dump_only=True)
    name=ma.String(required=True)


class UpdateInterestsSchema(InterestSchema):
    class Meta:
        model= Interest
        ordered = True
    id=ma.Integer(required=True)
    name=ma.String(required=True)
    @validates("id")
    def validate_interest_id(self,value):
       if Interest.get_interest_by_id(value) is None:
           raise ValidationError("No interest was found")
class AddInterestToTeacher(ma.SQLAlchemySchema):
    class Meta:
        model=Teacher
        ordered=True
    
    interest_id=fields.List(fields.Integer(),load_only=True,required=True)
    teacher_email=ma.String(required=True,load_only=True)
    id=ma.String(dump_only=True)
    name=ma.String(dump_only=True)
    @validates('interest_id')
    def validate_student_id(self,value):
        if Interest.get_interest_by_id(value) is None:
            raise ValidationError('No interest was found')
    @validates('teacher_email')
    def validate_teacher_email(self,value):
        if User.find_by_email(value) is None:
            raise ValidationError('No email was found')
        elif User.find_by_email(value).teacher is None:
            raise ValidationError('No teacher was found with this email was found')