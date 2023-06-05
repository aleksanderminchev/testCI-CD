from apifairy.decorators import other_responses
from flask import Blueprint, abort
from apifairy import authenticate, body, response

from models.program import Program
from models.teacher import Teacher
from api.schema.programs import ProgramsSchema, UpdateProgramsSchema, AddProgramToTeacher
from api.auth import token_auth, admin_auth, limit_user_to_own_routes_decorator
from api.decorators import paginated_response

programs = Blueprint('programs', __name__)
program_schema = ProgramsSchema()
programs_schema = ProgramsSchema(many=True)


@programs.route('/programs', methods=['POST'])
@authenticate(admin_auth)
@body(program_schema)
@response(program_schema, 201)
def new(args):
    # Should the child be attached to a customer
    """Creates a new program"""
    return Program.add_new_program(**args)


@programs.route('/program/<int:id>', methods=['DELETE'])
@authenticate(admin_auth)
@response(program_schema)
@other_responses({404: 'program not found'})
def delete_program(id):
    """Delete a program by id"""
    program = Program.delete_program(id) or abort(404)
    return program.to_dict()


@programs.route('/programs', methods=['GET'])
@limit_user_to_own_routes_decorator
@authenticate(token_auth)
@paginated_response(schema=programs_schema)
def all():
    """Retrieve all programs"""
    return Program.query


@programs.route('/program/<int:id>', methods=['GET'])
@authenticate(token_auth)
@response(program_schema)
@other_responses({404: 'program not found'})
def get(id):
    """Retrieve a program by id"""
    program = Program.get_program_by_id(id) or abort(404)
    return program.to_dict()


@programs.route('/update_program', methods=['PUT'])
@authenticate(admin_auth)
@body(UpdateProgramsSchema())
@response(UpdateProgramsSchema())
def put(data):
    # feed args into the object validate in schema before hand
    """Edit program information"""
    return Program.update_program(**data)


@programs.route('/add_program_to_teacher', methods=['POST'])
@authenticate(token_auth)
@response(AddProgramToTeacher(), 201)
@body(AddProgramToTeacher())
@other_responses({404: 'Programs not found'})
def take_program(args):
    """Adds the program to a teacher"""
    teacher = Teacher.get_teacher_by_email(args['teacher_email'])
    programs = []
    for i in args['program_id']:
        programs.append(Program.add_program_to_teacher(teacher, i).to_dict())
    return programs


@programs.route('/remove_program_from_teacher', methods=['POST'])
@authenticate(token_auth)
@response(AddProgramToTeacher(), 201)
@body(AddProgramToTeacher())
@other_responses({404: 'Programs not found'})
def remove_program(args):
    """Removes the program from a teacher"""
    return Program.remove_program_from_teacher(**args).to_dict()
