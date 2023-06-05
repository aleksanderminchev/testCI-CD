from apifairy.decorators import other_responses
from flask import Blueprint, abort
from apifairy import authenticate, body, response

from models.subjects import Subjects
from models.teacher import Teacher
from api.schema.subjects import SubjectsSchema, UpdateSubjectsSchema, AddSubjectToTeacher
from api.auth import token_auth, admin_auth, limit_user_to_own_routes_decorator
from api.decorators import paginated_response

subjects = Blueprint('subjects_api', __name__)
subjects_schema = SubjectsSchema()
subjectss_schema = SubjectsSchema(many=True)


@subjects.route('/subjectss', methods=['POST'])
@authenticate(admin_auth)
@body(subjects_schema)
@response(subjects_schema, 201)
def new(args):
    # Should the child be attached to a customer
    """Creates a new subjects and adds it to the the customers account"""
    return Subjects.add_new_subject(**args)


@subjects.route('/subjects/<int:id>', methods=['DELETE'])
@authenticate(admin_auth)
@response(subjects_schema)
@other_responses({404: 'subjects not found'})
def delete_subjects(id):
    """Delete a subjects by id"""
    subject = Subjects.delete_subject(id) or abort(404)
    return subject.to_dict()


@subjects.route('/subjectss', methods=['GET'])
@authenticate(token_auth)
@limit_user_to_own_routes_decorator
@paginated_response(schema=subjectss_schema)
def all():
    """Retrieve all subjectss"""
    return Subjects.query


@subjects.route('/subjects/<int:id>', methods=['GET'])
@authenticate(token_auth)
@response(subjects_schema)
@other_responses({404: 'subjects not found'})
def get(id):
    """Retrieve a subjects by id"""
    subject = Subjects.get_subject_by_id(id) or abort(404)
    return subject.to_dict()


@subjects.route('/update_subjects', methods=['PUT'])
@authenticate(admin_auth)
@body(UpdateSubjectsSchema())
@response(UpdateSubjectsSchema())
def put(data):
    """Edit subjects information"""
    return Subjects.update_subject(**data)


@subjects.route('/add_subject_to_teacher', methods=['POST'])
@authenticate(token_auth)
@response(AddSubjectToTeacher(), 201)
@body(AddSubjectToTeacher())
@other_responses({404: 'teacher not found'})
def take_subject(args):
    """Adds the subject to being taught by the teacher"""
    subjects = []
    teacher = Teacher.get_teacher_by_email(args['teacher_email'])
    for i in args['subject_id']:
        subjects.append(Subjects.add_subject_to_teacher(i, teacher).to_dict())
    return subjects


@subjects.route('/remove_subject_from_teacher', methods=['POST'])
@authenticate(token_auth)
@response(AddSubjectToTeacher(), 201)
@body(AddSubjectToTeacher())
@other_responses({404: 'teacher not found'})
def remove_subject(args):
    """Removes the subject from being taught by the teacher"""
    return Subjects.remove_subject_from_teacher(**args).to_dict()
