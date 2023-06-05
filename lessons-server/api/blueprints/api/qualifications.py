from apifairy.decorators import other_responses
from flask import Blueprint, abort
from apifairy import authenticate, body, response

from models.qualification import Qualification
from models.teacher import Teacher
from api.schema.qualifications import QualificationsSchema, UpdateQualificationsSchema, AddQualificationToTeacher
from api.auth import token_auth, admin_auth, limit_user_to_own_routes_decorator
from api.decorators import paginated_response

qualifications = Blueprint('qualifications', __name__)
qualification_schema = QualificationsSchema()
qualifications_schema = QualificationsSchema(many=True)


@qualifications.route('/qualifications', methods=['POST'])
@authenticate(admin_auth)
@body(qualification_schema)
@response(qualification_schema, 201)
def new(args):
    # Should the child be attached to a customer
    """Creates a new qualification"""
    return Qualification.add_new_qualification(**args)


@qualifications.route('/qualification/<int:id>', methods=['DELETE'])
@authenticate(admin_auth)
@response(qualification_schema)
@other_responses({404: 'qualification not found'})
def delete_qualification(id):
    """Delete a qualification by id"""
    qualification = Qualification.delete_qualification(id) or abort(404)
    return qualification.to_dict()


@qualifications.route('/qualifications', methods=['GET'])
@authenticate(token_auth)
@limit_user_to_own_routes_decorator
@paginated_response(schema=qualifications_schema)
def all():
    """Retrieve all qualifications"""
    return Qualification.query


@qualifications.route('/qualification/<int:id>', methods=['GET'])
@authenticate(token_auth)
@response(qualification_schema)
@other_responses({404: 'qualification not found'})
def get(id):
    """Retrieve a qualification by id"""
    qualification = Qualification.get_qualification_by_id(id) or abort(404)
    return qualification.to_dict()


@qualifications.route('/update_qualification', methods=['PUT'])
@authenticate(admin_auth)
@body(UpdateQualificationsSchema())
@response(UpdateQualificationsSchema())
def put(data):
    """Edit qualification information"""
    return Qualification.update_qualification(**data)


@qualifications.route('/add_qualification_to_teacher', methods=['POST'])
@authenticate(token_auth)
@body(AddQualificationToTeacher())
@response(qualifications_schema, 201)
@other_responses({404: 'Qualifications not found'})
def take_qualification(args):
    """Adds the qualification to a teacher"""
    qualifications = []
    teacher = Teacher.get_teacher_by_id(args['teacher_email'])
    for i in args:
        qualifications.append(
            Qualification.add_qualification_to_teacher(teacher, i).to_dict())
    return qualifications


@qualifications.route('/remove_qualification_from_teacher', methods=['POST'])
@authenticate(token_auth)
@body(AddQualificationToTeacher())
@response(AddQualificationToTeacher(), 201)
@other_responses({404: 'Qualifications not found'})
def remove_qualification(args):
    """Removes the qualification from a teacher"""
    return Qualification.remove_qualification_from_teacher(**args).to_dict()
