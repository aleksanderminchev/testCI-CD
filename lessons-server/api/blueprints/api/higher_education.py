from apifairy.decorators import other_responses
from flask import Blueprint, abort
from apifairy import authenticate, body, response
from api.auth import limit_user_to_own_routes_decorator, token_auth, admin_auth
from api import db
from models.higher_education_institution import HigherEducationInstitution
from models.higher_education_programme import HigherEducationProgramme
from api.schema.higher_education import HigherEducationInstitutionSchema, AttachHigherEduProgramme, AttachHigherEduInstitution, HigherEducationProgrammeSchema
from api.decorators import paginated_response


higher_education = Blueprint('higher_education', __name__)


@higher_education.route('/attach_higher_institution', methods=['POST'])
@authenticate(admin_auth)
@body(AttachHigherEduInstitution())
@response(HigherEducationInstitutionSchema())
def attach_higher_institution(args):
    """Attach a higher education institution to a teacher"""
    higher_edu_institution = HigherEducationInstitution.add_higher_edu_institution_to_teacher(
        higher_edu_institution_id=args['id'], teacher_email=args['teacher_email'])
    return higher_edu_institution


@higher_education.route('/remove_higher_institution', methods=['POST'])
@authenticate(admin_auth)
@body(AttachHigherEduInstitution())
@response(HigherEducationInstitutionSchema())
def remove_higher_institution(args):
    """Remove higher education institution from a teacher"""
    higher_edu_institution = HigherEducationInstitution.remove_higher_edu_institution_from_teacher(
        higher_edu_institution_id=args['id'], teacher_email=args['teacher_email'])
    return higher_edu_institution


@higher_education.route('/attach_higher_programme', methods=['POST'])
@authenticate(admin_auth)
@body(AttachHigherEduProgramme())
@response(HigherEducationProgrammeSchema())
def attach_higher_programme(args):
    """Attach higher education programme to the a teacher"""
    higher_edu_programme = HigherEducationProgramme.add_higher_edu_programme_to_teacher(
        higher_edu_programme_id=args['id'], teacher_email=args['teacher_email'])
    print(higher_edu_programme)
    return higher_edu_programme


@higher_education.route('/remove_higher_programme', methods=['POST'])
@authenticate(admin_auth)
@body(AttachHigherEduProgramme())
@response(HigherEducationProgrammeSchema())
def remove_higher_programme(args):
    """Remove higher education programme from a teacher"""

    higher_edu_programme = HigherEducationProgramme.remove_higher_edu_programme_from_teacher(
        higher_edu_programme_id=args['id'], teacher_email=args['teacher_email'])
    print(higher_edu_programme)
    return higher_edu_programme


@higher_education.route('/attach_many_higher_programme', methods=['POST'])
@authenticate(admin_auth)
@body(AttachHigherEduProgramme(many=True))
@response(HigherEducationProgrammeSchema(many=True))
def attach_many_higher_programmes(args):
    """Attach many higher education programmes to the a teacher"""
    print(args)
    higher_programmes = []
    for i in args:
        higher_programmes.append(HigherEducationProgramme.add_higher_edu_programme_to_teacher(
            higher_edu_programme_id=i['id'], teacher_email=i['teacher_email']))
    # higher_edu_programme =HigherEducationProgramme.add_higher_edu_programme_to_teacher(higher_edu_programme_id=args['id'],teacher_email=args['teacher_email'])
    # return higher_edu_programme
    return higher_programmes


@higher_education.route('/attach_many_higher_institutions', methods=['POST'])
@authenticate(admin_auth)
@body(AttachHigherEduInstitution(many=True))
@response(HigherEducationInstitutionSchema(many=True))
def attach_many_higher_institutions(args):
    """Attach many higher education institutions to the a teacher"""
    print(args)
    higher_institutions = []
    for i in args:
        higher_institutions.append(HigherEducationInstitution.add_higher_edu_institution_to_teacher(
            higher_edu_institution_id=i['id'], teacher_email=i['teacher_email']))
    # higher_edu_programme =HigherEducationProgramme.add_higher_edu_programme_to_teacher(higher_edu_programme_id=args['id'],teacher_email=args['teacher_email'])
    # return higher_edu_programme
    return higher_institutions


@higher_education.route('/get_all_institutions', methods=['GET'])
@authenticate(token_auth)
@limit_user_to_own_routes_decorator
@paginated_response(HigherEducationInstitutionSchema(many=True))
def all_institutions():
    """Retrieve all Higher Education Institutions"""
    return HigherEducationInstitution.query


@higher_education.route('/get_all_programmes', methods=['GET'])
@authenticate(token_auth)
@limit_user_to_own_routes_decorator
@paginated_response(HigherEducationProgrammeSchema(many=True))
def all_programmes():
    """Retrieve all Higher Education Programmes"""
    return HigherEducationProgramme.query
