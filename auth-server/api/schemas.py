from marshmallow import validate, validates, validates_schema, \
    ValidationError, fields

from api import ma
from api.auth import token_auth
from models.customer import Customer
from models.course import Course
from models.order import Order
from models.student import Student
import re
import phonenumbers
paginated_schema_cache = {}
query_schema_cache = {}


class EmptySchema(ma.Schema):
    pass


class DateTimePaginationSchema(ma.Schema):
    class Meta:
        ordered = True

    limit = ma.Integer()
    offset = ma.Integer()
    after = ma.DateTime(load_only=True)
    count = ma.Integer(dump_only=True)
    total = ma.Integer(dump_only=True)

    @validates_schema
    def validate_schema(self, data, **kwargs):
        if data.get('offset') is not None and data.get('after') is not None:
            raise ValidationError('Cannot specify both offset and after')


class StringQueryParams(ma.Schema):
    class Meta:
        ordered = True

    date = ma.String()


class StringPaginationSchema(ma.Schema):
    class Meta:
        ordered = True

    limit = ma.Integer()
    offset = ma.Integer()
    after = ma.Integer(load_only=True)
    count = ma.Integer(dump_only=True)
    total = ma.Integer(dump_only=True)

    @validates_schema
    def validate_schema(self, data, **kwargs):
        if data.get('offset') is not None and data.get('after') is not None:
            raise ValidationError('Cannot specify both offset and after')


class CustomerStringPaginationSchema(ma.Schema):
    class Meta:
        ordered = True
    status = ma.String(load_only=True)
    customer_type = ma.String(load_only=True)
    name = ma.String(load_only=True)
    limit = ma.Integer()
    offset = ma.Integer()
    after = ma.Integer(load_only=True)
    count = ma.Integer(dump_only=True)
    total = ma.Integer(dump_only=True)

    @validates_schema
    def validate_schema(self, data, **kwargs):
        if data.get('offset') is not None and data.get('after') is not None:
            raise ValidationError('Cannot specify both offset and after')


class StudentStringPaginationSchema(ma.Schema):
    class Meta:
        ordered = True
    status = ma.String(load_only=True)
    limit = ma.Integer()
    offset = ma.Integer()
    after = ma.Integer(load_only=True)
    count = ma.Integer(dump_only=True)
    total = ma.Integer(dump_only=True)

    @validates_schema
    def validate_schema(self, data, **kwargs):
        if data.get('offset') is not None and data.get('after') is not None:
            raise ValidationError('Cannot specify both offset and after')


class LessonsPaginationSchema(ma.Schema):
    class Meta:
        ordered = True
    from_date = ma.Date(load_only=True, required=False)
    to_date = ma.Date(load_only=True, required=False)
    limit = ma.Integer()
    offset = ma.Integer()
    after = ma.Integer(load_only=True)
    count = ma.Integer(dump_only=True)
    total = ma.Integer(dump_only=True)

    @validates_schema
    def validate_schema(self, data, **kwargs):
        if data.get('offset') is not None and data.get('after') is not None:
            raise ValidationError('Cannot specify both offset and after')


class TeacherStringPaginationSchema(ma.Schema):
    class Meta:
        ordered = True
    status = ma.String(load_only=True)
    limit = ma.Integer()
    offset = ma.Integer()
    after = ma.Integer(load_only=True)
    count = ma.Integer(dump_only=True)
    total = ma.Integer(dump_only=True)

    @validates_schema
    def validate_schema(self, data, **kwargs):
        if data.get('offset') is not None and data.get('after') is not None:
            raise ValidationError('Cannot specify both offset and after')


def PaginatedCollection(schema, pagination_schema=StringPaginationSchema):
    if schema in paginated_schema_cache:
        return paginated_schema_cache[schema]

    class PaginatedSchema(ma.Schema):
        class Meta:
            ordered = True

        pagination = ma.Nested(pagination_schema)
        data = ma.Nested(schema, many=True)

    PaginatedSchema.__name__ = 'Paginated{}'.format(schema.__class__.__name__)
    paginated_schema_cache[schema] = PaginatedSchema
    return PaginatedSchema


def QueryCollection(schema, query_schema=StringPaginationSchema):
    if schema in query_schema_cache:
        return query_schema_cache[schema]

    class QuerySchema(ma.Schema):
        class Meta:
            ordered = True

        data = ma.Nested(schema, many=True)

    QuerySchema.__name__ = 'Query{}'.format(schema.__class__.__name__)
    query_schema_cache[schema] = QuerySchema
    return QuerySchema


class TutorSchema(ma.Schema):
    class Meta:
        ordered = True

    uid = ma.Integer(required=False)
    email = ma.String(required=False, validate=[
        validate.Length(max=120),
        validate.Email()
    ])


class TokenSchema(ma.Schema):
    class Meta:
        ordered = True

    access_token = ma.String(required=True)
    refresh_token = ma.String()


class PasswordResetRequestSchema(ma.Schema):
    class Meta:
        ordered = True

    email = ma.String(required=True, validate=[validate.Length(max=120),
                                               validate.Email()])


class PasswordResetSchema(ma.Schema):
    class Meta:
        ordered = True

    token = ma.String(required=True)
    new_password = ma.String(required=True, validate=validate.Length(min=3))


class ProfileConfirmation (ma.Schema):
    class Meta:
        ordered = True
    token = ma.String(required=True)
    password = ma.String(required=True, validate=validate.Length(min=3))
    confirm = ma.String(required=True, validate=validate.Length(min=3))
    email = ma.String(required=True, validate=validate.Email())


class OpenaiSchema(ma.Schema):
    class Meta:
        ordered = True

    prompt = ma.String(required=True)
    temperature = ma.Integer(required=False)
    max_tokens = ma.Integer(required=False)
    n = ma.Integer(required=False)


class DalleSchema(ma.Schema):
    class Meta:
        ordered = True

    prompt = ma.String(required=True)
    n = ma.Integer(required=False)


class TeachworkStatusSchema(ma.Schema):
    class Meta:
        ordered = True

    id = ma.Integer(required=True)
    status = ma.String(required=True)


class TeachworkAddChildSchema(ma.Schema):
    class Meta:
        ordered = True

    # Required fields
    customer_id = ma.Integer(required=True)
    first_name = ma.String(required=True)
    last_name = ma.String(required=True)
    email = ma.String(required=True)
    mobile_phone = ma.String(required=True)

    # Optional
    default_teacher_ids = fields.List(fields.Integer(), required=False)
    default_location_id = ma.Integer(required=False)
    default_service_ids = fields.List(fields.Integer(), required=False)


class TeachworksFamilySchema(ma.Schema):
    class Meta:
        ordered = True

    # Required fields
    first_name = ma.String(required=True)
    last_name = ma.String(required=True)
    email = ma.String(required=True)
    mobile_phone = ma.String(required=True)


class TeachworksChildSchema(ma.Schema):
    class Meta:
        ordered = True

    # Required fields
    first_name = ma.String(required=True)
    last_name = ma.String(required=True)
    email = ma.String(required=True)
    mobile_phone = ma.String(required=True)

    # Optional
    default_teacher_ids = fields.List(fields.Integer(), required=False)
    default_location_id = ma.Integer(required=False)
    default_service_ids = fields.List(fields.Integer(), required=False)


class TeachworksIndependentSchema(ma.Schema):
    class Meta:
        ordered = True

    # Required fields
    first_name = ma.String(required=True)
    last_name = ma.String(required=True)
    email = ma.String(required=True)
    mobile_phone = ma.String(required=True)

    # Optional
    default_teacher_ids = fields.List(fields.Integer(), required=False)
    default_location_id = ma.Integer(required=False)
    default_service_ids = fields.List(fields.Integer(), required=False)
    crm_id = ma.Integer(required=False)
    course_id = ma.Integer(required=False)


class TeachworksFamilyAndChildSchema(ma.Schema):
    class Meta:
        ordered = True

    family = fields.Nested(TeachworksFamilySchema(), required=False)
    child = fields.Nested(TeachworksChildSchema(), required=False)
    crm_id = ma.Integer(required=False)
    course_id = ma.Integer(required=False)


class CourseSchema(ma.Schema):
    class Meta:
        ordered = True
        model = Course

    # Required fields
    subjects = ma.String(required=True)
    crm_deal_id = ma.Integer(required=True)
    course_type = ma.String(required=True)
    name = ma.String(required=True)
    hours_per_session = ma.Integer(required=True)
    weekly_frequency = ma.Integer(required=True)
    estimated_length = ma.String(required=True)

    # optional
    class_grade = ma.String(required=False)
    education = ma.String(required=False)
    math_programs = ma.String(required=False)
    comment = ma.String(required=False)
    unavailable_days = ma.String(required=False)
    hidden = ma.Boolean(required=False)
    taken_by = ma.Integer(
        required=False, description="ID of Teacher that the course is taken by.")
    status = fields.Str(required=True, validate=validate.OneOf(
        ["Pending", "Taken", "Cancelled"]))

    # Dump only
    id = ma.Integer(dump_only=True)
    hashed_id = ma.String(dump_only=True)


class OrderSchema(ma.SQLAlchemySchema):
    class Meta:
        ordered = True
        model = Order

    # Required fields
    total_hours = ma.Integer(required=True)
    package = ma.String(required=True)
    installments = ma.Integer(required=True)
    crm_deal_id = ma.String(required=False)
    email = ma.String(required=True)
    name = ma.String(required=True)
    email_sent = ma.Boolean(required=True)
    # # optional
    discount = ma.String(required=False)
    stripe_customer = ma.String(required=False)
    extra_student = ma.Integer(required=False)
    upsell = ma.Boolean(required=False)

    # # dump only
    status = ma.String(dump_only=True)
    total_price = ma.auto_field(dump_only=True)
    type_order = ma.String(dump_only=True)
    id = ma.Integer(dump_only=True)
    created_at = ma.auto_field(dump_only=True)
    last_updated = ma.auto_field(dump_only=True)
    booking_date = ma.auto_field(dump_only=True)
    balance_id = ma.auto_field(dump_only=True)
    customer_id = ma.auto_field(dump_only=True)


class UpdateOrderSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Order
        ordered = True
    uid = ma.Integer(required=True)
    total_hours = ma.Integer(required=False)
    package = ma.String(required=False)
    installments = ma.Integer(required=False)
    crm_deal_id = ma.String(required=False)
    email = ma.String(required=False)
    name = ma.String(required=False)
    status = ma.String(required=False, validate=validate.OneOf(
        ["pending", "paid", "void"]))
    email_sent = ma.Boolean(required=False)
    # optional
    discount = ma.String(required=False)
    stripe_customer = ma.String(required=False)
    extra_student = ma.Integer(required=False)
    total_price = ma.Integer(required=False)

    @validates('uid')
    def validate_user(self, value):
        if Order.get_order_by_id(id=value) is None:
            raise ValidationError('Invalid Order')


class CourseAddSchema(ma.Schema):
    class Meta:
        ordered = True

    # Required fields
    course = fields.Nested(CourseSchema())
    soft_filters = fields.Dict(required=False)
    hard_filters = fields.Dict(required=False)
    subjects = fields.List(fields.String(), required=False)


class TutorMatchSchema(ma.Schema):
    class Meta:
        ordered = True

    subjects = fields.List(fields.String(), required=False)
    soft_filters = fields.Dict(required=False)
    hard_filters = fields.Dict(required=False)


class UpdateCourseStatusSchema(ma.Schema):

    # Required fields
    hashed_id = ma.String(required=True)
    status = fields.Str(required=True, validate=validate.OneOf(
        ["Pending", "Taken", "Cancelled"]))


class UpdateCourseSchema(ma.Schema):
    class Meta:
        ordered = True
        model = Course
    id = ma.String(required=True, description="Hashed ID.")
    subjects = ma.String(required=False)
    crm_deal_id = ma.Integer(required=False)
    course_type = ma.String(required=False)
    name = ma.String(required=False)
    hours_per_session = ma.Integer(required=False)
    weekly_frequency = ma.Integer(required=False)
    estimated_length = ma.String(required=False)
    class_grade = ma.String(required=False)
    education = ma.String(required=False)
    comment = ma.String(required=False)
    unavailable_days = ma.String(required=False)
    taken_by = ma.Integer(required=False)
    status = fields.Str(required=False, validate=validate.OneOf(
        ["Pending", "Taken", "Cancelled"]))
