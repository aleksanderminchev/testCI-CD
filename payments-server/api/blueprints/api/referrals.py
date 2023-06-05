from apifairy.decorators import other_responses
from flask import Blueprint, abort
from apifairy import authenticate, body, response

from models.referral import Referral
from api.schema.referrals import ReferralSchema, UpdateReferralsSchema, AddReferral
from api.auth import token_auth, admin_auth
from api.decorators import paginated_response

referrals = Blueprint('referrals', __name__)
referral_schema = ReferralSchema()
referrals_schema = ReferralSchema(many=True)


@referrals.route('/referrals', methods=['POST'])
@authenticate(admin_auth)
@body(AddReferral())
@response(referral_schema, 201)
def new(args):
    """Creates a new referral for a teacher, the reffered teacher has to be created"""
    return Referral.add_new_referral(**args)


@referrals.route('/referral/<int:id>', methods=['DELETE'])
@authenticate(admin_auth)
@response(referral_schema)
@other_responses({404: 'referral not found'})
def delete_referral(id):
    """Delete a referral by id"""
    referral = Referral.delete_referral(id) or abort(404)
    return referral.to_dict()


@referrals.route('/referrals', methods=['GET'])
@authenticate(token_auth)
@paginated_response(schema=referrals_schema)
def all():
    """Retrieve all referrals"""
    return Referral.query


@referrals.route('/referral/<int:id>', methods=['GET'])
@authenticate(token_auth)
@response(referral_schema)
@other_responses({404: 'referral not found'})
def get(id):
    """Retrieve a referral by id"""
    referral = Referral.get_referral_by_id(id) or abort(404)
    return referral.to_dict()


@referrals.route('/update_referral', methods=['PUT'])
@authenticate(admin_auth)
@body(UpdateReferralsSchema())
@response(UpdateReferralsSchema())
def put(data):
    # feed args into the object validate in schema before hand
    """Edit referral information"""
    return Referral.update_referral(**data)
