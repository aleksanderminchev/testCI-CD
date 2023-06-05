"""
To integrate with Flask- HTTPAuth, the application needs to provide two functions:
one that defines the logic to check the email and password provided by the user,
and another that returns the error response in the case of an authentication failure.

For the user login those are verify_password() and basic_auth_error().
For the API those are verify_token() and error_handler().

These functions are registered with Flask-HTTPAuth through decorators,
and then are automatically called by the extension as needed during the authentication flow.
"""

from flask import current_app, request, make_response, jsonify
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from functools import wraps
from werkzeug.exceptions import Unauthorized, Forbidden

from api.app import db
from models.user import User

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()
admin_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(email, password):
    """ User is then available as basic_auth.current_user()"""
    if email and password:
        user = User.get_user(email, password)
        if user:
            return user


@basic_auth.error_handler
def basic_auth_error(status=401):
    error = (Forbidden if status == 403 else Unauthorized)()
    return {
        'code': error.code,
        'message': error.name,
        'description': error.description,
    }, error.code, {'WWW-Authenticate': 'Form'}


@token_auth.verify_token
def verify_token(access_token):
    if current_app.config['DISABLE_AUTH']:
        user = db.session.get(User, 1)
        return user
    if access_token:
        return User.verify_access_token(access_token)


@token_auth.error_handler
def token_auth_error(status=401):
    error = (Forbidden if status == 403 else Unauthorized)()
    return {
        'code': error.code,
        'message': error.name,
        'description': error.description,
    }, error.code


@admin_auth.verify_token
def verify_admin_token(token):
    if token:
        # Check access token
        user = User.verify_access_token(token)
        if user is not None:
            if user.is_admin:
                return user

        # Admin API JWT Token
        user = User.verify_api_jwt_token(token)
        if user is not None:
            if user.is_admin:
                return user

    return None


@admin_auth.error_handler
def token_admin_auth_error(status=401):
    error = (Forbidden if status == 403 else Unauthorized)()
    return {
        'code': error.code,
        'message': error.name,
        'description': error.description,
    }, error.code


def limit_user_to_own_routes_decorator(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        # Add a user dict to get the routes that a user can access
        # function within user which checks the type and gives back a dict with allowed routes
        # then abort if the request url doesn't match the allowed routes
        if request.headers['Authorization']:
            user = User.verify_access_token(
                request.headers['Authorization'].split(' ')[1])
            routes_allowed = user.routes_allowed()
            print(request.full_path[:-1])
            if "*" in routes_allowed:
                return f(*args, **kwargs)
            elif request.full_path[:-1] in routes_allowed:
                return f(*args, **kwargs)
            else:
                return make_response(jsonify({"message": "Blocked access, you do not permission to access this route."}), 500)
        return f(*args, **kwargs)
    return decorator
