
from datetime import datetime, timezone
from marshmallow import validate, validates, validates_schema, \
    ValidationError, fields

from api import ma
from models.high_school import HighSchool
from models.user import User


class HighSchoolSchema(ma.SQLAlchemySchema):
    class Meta():
        model = HighSchool
        ordered = True
    id = ma.Integer()
    name = ma.String(dump_only=True)


class AttachHighSchool(HighSchoolSchema):
    class Meta():
        model = HighSchool
        ordered = True
    teacher_email = ma.String()

    @validates('id')
    def validate_student_id(self, value):
        if HighSchool.query.get(value) is None:
            raise ValidationError('No higher education was found')

    @validates('teacher_email')
    def validate_teacher_email(self, value):
        if User.find_by_email(value) is None:
            raise ValidationError('No email was found')
        elif User.find_by_email(value).teacher is None:
            raise ValidationError(
                'No teacher was found with this email was found')
