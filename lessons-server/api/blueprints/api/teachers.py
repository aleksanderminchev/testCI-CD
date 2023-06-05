from apifairy.decorators import other_responses
from flask import Blueprint, abort
from apifairy import authenticate, body, response
from api import db
from sqlalchemy.orm import joinedload, contains_eager

from models.teacher import Teacher
from api.schema.teacher.teachers import TeacherSchema, AddStudentToTeacher, \
    FilterTeacherShema, UpdateTeacherSchema, CalendarTeacher
from api.schema.teacher.create_teacher import CreateTeacherSchema
from api.schema.user import UserSchema
from api.auth import token_auth
from api.schema.student import StudentSchema, GetLessonSpace
from api.decorators import paginated_response, query_params
from api.utils.lessonspace import create_user_jwt_url
from api.schemas import TeacherStringPaginationSchema

teachers = Blueprint('teachers', __name__)
teacher_schema = TeacherSchema()
create_teacher_schema = CreateTeacherSchema()
teachers_schema = TeacherSchema(many=True)
update_teacher_schema = UpdateTeacherSchema(partial=True)
users_schema = UserSchema(many=True)


@teachers.route('/teachers', methods=['POST'])
@body(create_teacher_schema)
@response(create_teacher_schema, 201)
def new(args):
    """Creates a new teacher"""
    teacher = Teacher.add_new_teacher(**args)
    return teacher.to_dict()


@teachers.route('/teacher/<int:id>', methods=['DELETE'])
# @authenticate(token_auth)
@response(teacher_schema)
@other_responses({404: 'teacher not found'})
def delete_teacher(id):
    """Delete a teacher by id"""
    return Teacher.delete_teacher(id) or abort(404)


@teachers.route('/teachers', methods=['GET'])
# @authenticate(token_auth)
@paginated_response(schema=teacher_schema, pagination_schema=TeacherStringPaginationSchema)
def all():
    """GET all teachers
    Applies pagination for getting all teachers.
    """
    from models.lesson import Lesson
    from models.student import Student
    from models.higher_education_institution import HigherEducationInstitution
    from models.higher_education_programme import HigherEducationProgramme
    if 'active' == request.args.get('status'):
        return Teacher.query.options(
            joinedload(Teacher.students),
            joinedload(Teacher.higher_education_programmes),
            joinedload(Teacher.higher_education_institutions),
            joinedload(Teacher.subjects),
            joinedload(Teacher.interests)
        ).filter_by(status=request.args.get('status'))

    return Teacher.query


@teachers.route('/teachers/<int:id>', methods=['GET'])
# @authenticate(token_auth)
@response(teacher_schema)
@other_responses({404: 'teacher not found'})
def get(id):
    """Retrieve a teacher by id"""
    teacher = Teacher.get_teacher_by_id(id) or abort(404)
    print(teacher.lessons_teacher)
    return teacher.to_dict()


@teachers.route('/take_student', methods=['POST'])
# @authenticate(token_auth)
@response(AddStudentToTeacher(many=True), 201)
@body(AddStudentToTeacher())
@other_responses({404: 'teacher not found'})
def take_student(args):
    """Adds the student to being taught by the teacher"""
    return Teacher.add_student_to_teacher(**args)


@teachers.route('/remove_student', methods=['POST'])
# @authenticate(token_auth)
@response(AddStudentToTeacher(many=True), 201)
@body(AddStudentToTeacher())
@other_responses({404: 'teacher not found'})
def remove_student(args):
    """Removes the student from being taught by the teacher"""
    return Teacher.remove_student_from_teacher(**args)


@teachers.route('/teachers/<email>', methods=['GET'])
# @authenticate(token_auth)
@response(teacher_schema)
@other_responses({404: 'teacher not found'})
def get_by_email(email):
    """Retrieves the teachers by the email address provided of the user"""
    return Teacher.get_teacher_by_email(email).to_dict() or abort(404)


@teachers.route('/teachers-calendar', methods=['GET'])
# @authenticate(token_auth)
@query_params(CalendarTeacher(many=True), CalendarTeacher())
@other_responses({404: 'lesson not found'})
def get_all_teachers_for_calendar(args):
    """Retrieves all the teachers for the calendar"""
    status = 'active'
    if 'filter_status' in args.keys():
        status = args['filter_status']
    teachers = Teacher.query.filter_by(status=status)
    data = [i.to_calendar() for i in (teachers or [])]
    return {'data': data}


@teachers.route('/update_teacher', methods=['PUT'])
# @authenticate(token_auth)
@body(update_teacher_schema)
@response(update_teacher_schema)
def put(data):
    # feed args into the object validate in schema before hand
    """Edit teacher information"""
    return Teacher.update_teacher(**data)


@teachers.route('/filter_teachers', methods=['POST'])
@body(FilterTeacherShema())
@response(FilterTeacherShema(many=True), 201)
def filter_teachers(args):
    # Should the child be attached to a customer
    """Filters the teacher based on the provided parameters
    Returns the teachers in array format,
    if given an empty body will just return all the teachers
    """
    teacher = Teacher.filter_teachers(**args)
    return teacher


@teachers.route('/get_all_students/<email>', methods=['GET'])
@response(StudentSchema(many=True), 201)
def get_all_students_of_teacher(email):
    """Retrive all students of the teacher that are active"""
    teacher = Teacher.get_teacher_by_email(email)
    students = []
    for i in teacher.students:
        print(i.status.value)
        if i.status.value == 'active':
            students.append(i.to_dict())
    return students


@teachers.route('/get_lesson_space_url_teacher/<int:id>', methods=['GET'])
# @authenticate(token_auth)
@response(GetLessonSpace())
@other_responses({404: 'lesson not found'})
def lessons_space(id):
    """Generates the url for the lesson space for the teacher"""
    from models.lesson import Lesson
    lesson = Lesson.get_lesson_by_id(id) or abort(404)
    url = create_user_jwt_url(lesson.lessons_teacher,
                              lesson.space, lesson.secret, 'teacher')
    return {"url": url}
