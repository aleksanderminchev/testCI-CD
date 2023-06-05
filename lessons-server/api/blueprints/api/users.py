from flask import Blueprint, abort, current_app, render_template
from apifairy import authenticate, body, response, other_responses

from api import db
from models.user import User
from api.schema.user import UserSchema, UpdateUserSchema
from api.schemas import PasswordResetRequestSchema
from api.auth import token_auth, limit_user_to_own_routes_decorator, admin_auth
from api.decorators import paginated_response
from api.email import send_email

users = Blueprint('users', __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)
update_user_schema = UpdateUserSchema(partial=True)


@users.route('/users', methods=['POST'])
@authenticate(admin_auth)
@body(user_schema)
@response(user_schema, 201)
def new(args):
    """Register a new user.

    Anyone can register a new user.

    There's E-mail validation.

    There's Phone validation.
    """
    user = User(**args)
    db.session.add(user)
    db.session.commit()
    return user


@users.route('/users', methods=['GET'])
@authenticate(token_auth)
@paginated_response(users_schema)
def all():
    """Retrieve all users"""
    return User.query


@users.route('/users/<int:id>', methods=['GET'])
@authenticate(token_auth)
@response(user_schema)
@other_responses({404: 'User not found'})
def get(id):
    """Retrieve a user by id"""
    return db.session.get(User, id).to_dict() or abort(404)


@users.route('/users/<email>', methods=['GET'])
@authenticate(token_auth)
@limit_user_to_own_routes_decorator
@response(user_schema)
@other_responses({404: 'User not found'})
def get_by_email(email):
    """Retrieve a user by email"""
    return User.query.filter_by(email=email).first() or \
        abort(404)


@users.route('/me', methods=['GET'])
@authenticate(token_auth)
@response(user_schema)
def me():
    """Retrieve the authenticated user"""
    print(user_schema)
    return token_auth.current_user().to_dict()


@users.route('/me', methods=['PUT'])
@authenticate(token_auth)
@body(update_user_schema)
@response(user_schema)
def put(data):
    """Edit user information"""
    user = token_auth.current_user()
    if 'password' in data and ('old_password' not in data or
                               not user.verify_password(data['old_password'])):
        abort(400)
    user.update(data)
    print(user.token)
    db.session.commit()
    return user


@users.route('/resendEmail', methods=['POST'])
@authenticate(admin_auth)
@body(PasswordResetRequestSchema)
@response(user_schema, 200)
def sendEmail(data):
    """Resend the verification email for the users"""
    user = User.find_by_email(data['email'])
    if user is not None:
        reset_token = user.generate_reset_token()
        reset_url = current_app.config['CONFIRMATION_URL'] + \
            '?token=' + reset_token
        template = render_template(
            "email/verify-email.html",
            token=reset_token,
            confirm_url=reset_url
        )
        send_email([data['email']], 'Confirm your account', template)
        return user.to_dict()
    else:
        abort(400)
