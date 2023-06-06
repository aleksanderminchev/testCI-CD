from marshmallow import validate, validates, validates_schema, \
    ValidationError, fields

from api import ma
from api.auth import token_auth
from models.qualification import Qualification
from models.user import User
from models.teacher import Teacher


class QualificationsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Qualification
        ordered = True
    id = ma.Integer(dump_only=True)
    name = ma.String(required=True)


class UpdateQualificationsSchema(QualificationsSchema):
    class Meta:
        model = Qualification
        ordered = True
    id = ma.Integer(required=True)
    name = ma.String(required=True)

    @validates("id")
    def validate_qualifications_id(self, value):
        if Qualification.get_qualification_by_id(value) is None:
            raise ValidationError("No qualification was found")


class AddQualificationToTeacher(ma.SQLAlchemySchema):
    class Meta:
        model = Teacher
        ordered = True

    qualification_id = fields.List(
        fields.Integer(), load_only=True, required=True)
    teacher_email = ma.String(required=True, load_only=True)
    id = ma.String(dump_only=True)
    name = ma.String(dump_only=True)

    @validates('qualification_id')
    def validate_student_id(self, value):
        if Qualification.get_qualification_by_id(value) is None:
            raise ValidationError('No subject was found')

    @validates('teacher_email')
    def validate_teacher_email(self, value):
        if User.find_by_email(value) is None:
            raise ValidationError('No email was found')
        elif User.find_by_email(value).teacher is None:
            raise ValidationError(
                'No teacher was found with this email was found')
