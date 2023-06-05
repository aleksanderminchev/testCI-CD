from apifairy.decorators import other_responses
from flask import Blueprint, abort
from apifairy import authenticate, body, response
from api.auth import limit_user_to_own_routes_decorator, token_auth, admin_auth
from api import db
from models.high_school import HighSchool
from api.schema.highschool import HighSchoolSchema, AttachHighSchool
from api.decorators import paginated_response
high_school = Blueprint('high_school', __name__)


@high_school.route('/attach_high_school', methods=['POST'])
@authenticate(admin_auth)
@body(AttachHighSchool())
@response(HighSchoolSchema())
def attach_high_school(args):
    """Attach a high school to a teacher"""
    highschool = HighSchool.add_high_school_to_teacher(
        high_school_id=args['id'], teacher_email=args['teacher_email'])
    return highschool


@high_school.route('/remove_high_school', methods=['POST'])
@authenticate(admin_auth)
@body(AttachHighSchool())
@response(HighSchoolSchema())
def remove_high_school(args):
    """Remove high school from a teacher"""
    highschool = HighSchool.remove_high_school_from_teacher(
        highschool_id=args['id'], teacher_email=args['teacher_email'])
    return highschool


@high_school.route('/attach_many_high_schools', methods=['POST'])
@authenticate(admin_auth)
@body(AttachHighSchool(many=True))
@response(HighSchoolSchema(many=True))
def attach_many_high_schools(args):
    """Attach many high schools to the a teacher"""
    print(args)
    high_schools = []
    for i in args:
        high_schools.append(HighSchool.add_high_school_to_teacher(
            highschool_id=i['id'], teacher_email=i['teacher_email']))
    # higher_edu_programme =HigherEducationProgramme.add_higher_edu_programme_to_teacher(higher_edu_programme_id=args['id'],teacher_email=args['teacher_email'])
    # return higher_edu_programme
    return high_schools


@high_school.route('/get_all_highschools', methods=['GET'])
@authenticate(admin_auth)
@limit_user_to_own_routes_decorator
@paginated_response(HighSchoolSchema(many=True))
def all_high_school():
    """Retrieve all High schools"""
    return HighSchool.query
