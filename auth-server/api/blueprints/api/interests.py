from apifairy.decorators import other_responses
from flask import Blueprint, abort
from apifairy import authenticate, body, response

from api import db
from models.interest import Interest
from models.teacher import Teacher
from api.schema.interests import InterestSchema, UpdateInterestsSchema, AddInterestToTeacher
from api.auth import token_auth, admin_auth, limit_user_to_own_routes_decorator
from api.decorators import paginated_response

interests = Blueprint('interests', __name__)
interest_schema = InterestSchema()
interests_schema = InterestSchema(many=True)


@interests.route('/interests', methods=['POST'])
@authenticate(admin_auth)
@body(interest_schema)
@response(interest_schema, 201)
def new(args):
    # Should the child be attached to a customer
    """Creates a new interest and adds it to the the customers account"""
    return Interest.add_new_interest(**args)


@interests.route('/interest/<int:id>', methods=['DELETE'])
@authenticate(admin_auth)
@response(interest_schema)
@other_responses({404: 'interest not found'})
def delete_interest(id):
    """Delete a interest by id"""
    interest = Interest.delete_interest(id) or abort(404)
    return interest.to_dict()


@interests.route('/interests', methods=['GET'])
@limit_user_to_own_routes_decorator
@authenticate(token_auth)
@paginated_response(schema=interests_schema)
def all():
    """Retrieve all interests"""
    return Interest.query


@interests.route('/interest/<int:id>', methods=['GET'])
@authenticate(token_auth)
@response(interest_schema)
@other_responses({404: 'interest not found'})
def get(id):
    """Retrieve a interest by id"""
    interest = Interest.get_interest_by_id(id) or abort(404)
    return interest.to_dict()


@interests.route('/update_interest', methods=['PUT'])
@authenticate(admin_auth)
@body(UpdateInterestsSchema())
@response(UpdateInterestsSchema())
def put(data):
    # feed args into the object validate in schema before hand
    """Edit interest information"""
    return Interest.update_interest(**data)


@interests.route('/add_interest_to_teacher', methods=['POST'])
@authenticate(token_auth)
@response(interests_schema, 201)
@body(AddInterestToTeacher())
@other_responses({404: 'interests not found'})
def take_interest(args):
    """Adds the interest to a teacher"""
    interests = []
    teacher = Teacher.get_teacher_by_email(args['teacher_email'])
    for i in args['interest_id']:
        interests.append(
            Interest.add_interest_to_teacher(teacher, i).to_dict())
    return interests


@interests.route('/remove_interest_from_teacher', methods=['POST'])
@authenticate(token_auth)
@response(AddInterestToTeacher(), 201)
@body(AddInterestToTeacher())
@other_responses({404: 'interests not found'})
def remove_interest(args):
    """Removes the interest from a teacher"""
    return Interest.remove_interest_from_teacher(**args).to_dict()
