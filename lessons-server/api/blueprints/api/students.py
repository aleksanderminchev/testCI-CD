from apifairy.decorators import other_responses
from flask import Blueprint, abort, request
from apifairy import authenticate, body, response

from models.student import Student
from api.schemas import StudentStringPaginationSchema
from api.schema.student import GetLessonSpace, StudentSchema, AddTeacherToStudent, CreateStudentSchema, UpdateStudentSchema, CreateStudentYoungSchema
from api.schema.teacher.teachers import TeacherSchema
from api.auth import token_auth, limit_user_to_own_routes_decorator, admin_auth
from api.decorators import paginated_response
from api.utils.lessonspace import create_user_jwt_url


students = Blueprint('students', __name__)
student_schema = StudentSchema()
create_student_schema = CreateStudentSchema()
students_schema = StudentSchema(many=True)
update_student_schema = UpdateStudentSchema(partial=True)

# use this to add a student with an email to the customer account
# the student does not have its own account


@students.route('/student_with_user', methods=['POST'])
@authenticate(admin_auth)
@body(create_student_schema)
@response(create_student_schema, 201)
def new_student(args):
    # Should the child be attached to a customer
    """Creates a new student and adds it to the the customers account 
    with a user account"""
    student = Student.add_new_student(typeOfStudent='with_user', **args)
    return student.to_dict()
# use this to create a student with an email to the customer account
# create a user account for him as well


@students.route('/student', methods=['POST'])
@authenticate(admin_auth)
@body(CreateStudentYoungSchema())
@response(CreateStudentYoungSchema(), 201)
def new_student_with_user(args):
    """Creates a new student and adds it to the the customers account
    no user account"""
    student= Student.add_new_student(typeOfStudent='no_user', **args)
    return student.to_dict()


@students.route('/student/<int:id>', methods=['DELETE'])
@authenticate(admin_auth)
@response(student_schema)
@other_responses({404: 'Student not found'})
def delete_student(id):
    """Delete a student by id"""
    student = Student.delete_student(id) or abort(404)
    return student.to_dict()


@students.route('/students', methods=['GET'])
@authenticate(token_auth)
@paginated_response(students_schema, pagination_schema=StudentStringPaginationSchema())
def all():
    """Retrieve all students"""
    if 'active' == request.args.get('status'):
        return Student.query.filter_by(status=request.args.get('status'))
    return Student.query


@students.route('/students/<int:id>', methods=['GET'])
@limit_user_to_own_routes_decorator
@authenticate(token_auth)
@response(student_schema)
@other_responses({404: 'student not found'})
def get(id):
    """Retrieve a student by id"""
    return Student.get_student_by_id(id).to_dict() or abort(404)


@students.route('/students/<email>', methods=['GET'])
@limit_user_to_own_routes_decorator
@authenticate(token_auth)
@response(students_schema)
@other_responses({404: 'student not found'})
def get_by_email(email):
    """Retrieves the students by the email address"""
    students = Student.get_student_by_email(email) or abort(404)
    return [i.to_dict() for i in students]


@students.route('/take_teachers', methods=['POST'])
@authenticate(token_auth)
@body(AddTeacherToStudent())
@response(AddTeacherToStudent(many=True), 201)
@other_responses({404: 'teacher not found'})
def take_teachers(args):
    """Assigns teachers to student
    """
    return Student.add_teacher_to_student(**args)


@students.route('/get_all_teachers/<email>', methods=['GET'])
@authenticate(token_auth)
@limit_user_to_own_routes_decorator
@response(TeacherSchema(many=True), 201)
def get_all_students_of_teacher(email):
    """Retrive all teachers of the students that are active"""
    students = Student.get_student_by_email(email)
    teachers = set()
    for i in students:
        for j in i.teachers:
            print(j)
            if j.status.value == 'active':
                teachers.add(j)
    return [i.to_dict() for i in teachers]


@students.route('/student', methods=['PUT'])
@authenticate(token_auth)
@body(update_student_schema)
@response(update_student_schema)
def put(data):
    # feed args into the object validate in schema before hand
    """Edit student information"""
    student = Student.update_student(**data) or abort(404)
    return student.to_dict()


@students.route('/get_lesson_space_url_student/<int:id>', methods=['GET'])
@authenticate(token_auth)
@limit_user_to_own_routes_decorator
@response(GetLessonSpace())
@other_responses({404: 'lesson not found'})
def lessons_space(id):
    """Generates the url for the lesson space for the student"""
    from models.lesson import Lesson
    lesson = Lesson.get_lesson_by_id(id) or abort(404)
    url = create_user_jwt_url(
        lesson.lessons_students[0], lesson.space, lesson.secret, 'student')
    return {"url": url}
