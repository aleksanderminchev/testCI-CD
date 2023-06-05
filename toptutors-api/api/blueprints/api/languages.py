from apifairy.decorators import other_responses
from flask import Blueprint, abort
from apifairy import authenticate, body, response

from api import db
from models.language import Language
from models.teacher import Teacher
from api.schema.languages import LanguageSchema, UpdateLanguagesSchema, AddLanguageToTeacher
from api.auth import token_auth, admin_auth, limit_user_to_own_routes_decorator
from api.decorators import paginated_response

languages = Blueprint('languages', __name__)
language_schema = LanguageSchema()
languages_schema = LanguageSchema(many=True)


@languages.route('/languages', methods=['POST'])
@authenticate(admin_auth)
@body(language_schema)
@response(language_schema, 201)
def new(args):
    # Should the child be attached to a customer
    """Creates a new language and adds it to the the customers account"""
    return Language.add_new_language(**args)


@languages.route('/language/<int:id>', methods=['DELETE'])
@authenticate(admin_auth)
@response(language_schema)
@other_responses({404: 'language not found'})
def delete_language(id):
    """Delete a language by id"""
    language = Language.delete_language(id) or abort(404)
    return language.to_dict()


@languages.route('/languages', methods=['GET'])
@limit_user_to_own_routes_decorator
@authenticate(token_auth)
@paginated_response(schema=languages_schema)
def all():
    """Retrieve all languages"""
    return Language.query


@languages.route('/language/<int:id>', methods=['GET'])
@authenticate(token_auth)
@response(language_schema)
@other_responses({404: 'language not found'})
def get(id):
    """Retrieve a language by id"""
    language = Language.get_language_by_id(id) or abort(404)
    return language.to_dict()


@languages.route('/update_language', methods=['PUT'])
@authenticate(admin_auth)
@body(UpdateLanguagesSchema())
@response(UpdateLanguagesSchema())
def put(data):
    # feed args into the object validate in schema before hand
    """Edit language information"""
    return Language.update_language(**data)


@languages.route('/add_language_to_teacher', methods=['POST'])
@authenticate(token_auth)
@response(languages_schema, 201)
@body(AddLanguageToTeacher())
@other_responses({404: 'languages not found'})
def take_language(args):
    """Adds the language to a teacher"""
    print(args)
    languages = []
    teacher = Teacher.get_teacher_by_email(args['teacher_email'])
    for i in args['language_id']:
        languages.append(
            Language.add_language_to_teacher(teacher, i).to_dict())
    return languages


@languages.route('/remove_language_from_teacher', methods=['POST'])
@authenticate(token_auth)
@response(AddLanguageToTeacher(), 201)
@body(AddLanguageToTeacher())
@other_responses({404: 'languages not found'})
def remove_language(args):
    """Removes the language from a teacher"""
    return Language.remove_language_from_teacher(**args).to_dict()
