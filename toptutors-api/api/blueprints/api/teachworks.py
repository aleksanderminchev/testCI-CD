from flask import request, current_app, Blueprint
from decouple import config
from apifairy import authenticate, other_responses, body, response
# Internal imports
from api.services.tw import tw_api_utils
from api.schemas import TeachworkStatusSchema, TeachworkAddChildSchema, TeachworksFamilySchema, TeachworksFamilyAndChildSchema, TeachworksIndependentSchema
from api.auth import admin_auth


teachworks = Blueprint('Teachworks', __name__)


@teachworks.route("/change_customer_status", methods=["PUT"])
@authenticate(admin_auth)
@body(TeachworkStatusSchema)
@response(TeachworkStatusSchema)
@other_responses({401: 'Bad request: error in body.'})
def change_tw_status(user):
    """ Changes a customer's TW Status.

    Payload has to be a dictionary with TW id and string of new status (Active, Inactive, or Prospective).
    """
    filters = request.json
    if filters["id"] and filters["status"]:
        # In production we use RQ
        payload = {"customer": {
            "status": filters["status"]
        }
        }
        if config("CONFIG_NAME") == "production":
            current_app.task_queue.enqueue_call(
                func=tw_api_utils.put_to_tw,
                args=(f"customers/{filters['id']}", payload),
                result_ttl=5000,
            )
        else:
            tw_api_utils.put_to_tw(f"customers/{filters['id']}", payload)
        return {"id": filters["id"], "status": filters["status"]}


@teachworks.route("/add_child", methods=["POST"])
@authenticate(admin_auth)
@body(TeachworkAddChildSchema)
@other_responses({401: 'Bad request: error in body.'})
def add_child(user):
    """ Adds a student child to a TW customer.
    """
    filters = request.json
    payload = {
        "customer_id": filters["customer_id"],
        "first_name": filters["first_name"],
        "last_name": filters["last_name"],
        "email": filters["email"],
        "mobile_phone": filters["mobile_phone"],
        "status": "Active",
        "calender_color": "#0A61F7",
        "billing_method": "Package",
        "email_lesson_reminders": True,
        "email_lesson_notes": True,
    }

    # Optional fields
    if "default_location_id" in filters:
        payload["default_location_id"] = filters["default_location_id"]

    if "default_service_ids" in filters:
        payload["default_service_ids"] = filters["default_service_ids"]

    if "default_teacher_ids" in filters:
        payload["default_teacher_ids"] = filters["default_teacher_ids"]

    if config("CONFIG_NAME") == "production":
        current_app.task_queue.enqueue_call(
            func=tw_api_utils.add_to_tw,
            args=("/students", payload),
            result_ttl=5000,
        )
        return {"customer_id": filters["id"]}
    else:
        tw_api_utils.add_to_tw("/students", payload)
        return {"customer_id": filters["customer_id"]}


@teachworks.route("/add_family", methods=["POST"])
@authenticate(admin_auth)
@body(TeachworksFamilySchema)
@other_responses({401: 'Bad request: error in body.'})
def add_family(user):
    """ Adds a family (without a child) to TW.
    """
    filters = request.json
    payload = {
        "first_name": filters["first_name"],
        "last_name": filters["last_name"],
        "email": filters["email"],
        "mobile_phone": filters["mobile_phone"],
        "status": "Active",
        "calender_color": "#0A61F7",
        "billing_method": "Package",
        "email_lesson_reminders": True,
        "email_lesson_notes": True,
        "welcome_email": True,
        "enable_user_account": True,
    }

    if config("CONFIG_NAME") == "production":
        current_app.task_queue.enqueue_call(
            func=tw_api_utils.add_to_tw,
            args=("/customers/family", payload),
            result_ttl=5000,
        )
        return "Success!"
    else:
        tw_api_utils.add_to_tw("/customers/family", payload)
        return "Success!"


@teachworks.route("/add_family_with_child", methods=["POST"])
@authenticate(admin_auth)
@body(TeachworksFamilyAndChildSchema)
@other_responses({401: 'Bad request: error in body.'})
def add_family_with_child(user):
    """ Adds a family and assigns them a child student to TW.
    """

    family = request.json["family"]
    child = request.json["child"]

    payload_family = {
        "first_name": family["first_name"],
        "last_name": family["last_name"],
        "email": family["email"],
        "mobile_phone": family["mobile_phone"],
        "email_lesson_reminders": True,
        "email_lesson_notes": True,
        "welcome_email": True,
        "enable_user_account": True,
        "status": "Active",
        "billing_method": "Package",
    }

    payload_child = {
        "first_name": child["first_name"],
        "last_name": child["last_name"],
        "email": child["email"],
        "mobile_phone": child["mobile_phone"],
        "status": "Active",
        "calender_color": "#0A61F7",
        "billing_method": "Package",
    }

    # Optional fields
    if "default_location_id" in child:
        payload_child["default_location_id"] = child["default_location_id"]

    if "default_service_ids" in child:
        payload_child["default_service_ids"] = child["default_service_ids"]

    if "default_teacher_ids" in child:
        payload_child["default_teacher_ids"] = child["default_teacher_ids"]

        # If the family and student email is not the same then enable the account.
    if child["email"] != family["email"]:
        enable_user_account = {
            "welcome_email": True,
            "enable_user_account": True,
            "email_lesson_reminders": True,
            "email_lesson_notes": True,
        }
        payload_child.update(enable_user_account)

    if "course_id" in request.json:
        course_id = request.json["course_id"]
    else:
        course_id = None

    if "crm_id" in request.json:
        crm_id = request.json["crm_id"]
    else:
        crm_id = None

    if config("CONFIG_NAME") != "production":  # in development we run this
        response = tw_api_utils.add_family_with_child(
            payload_child, payload_family, crm_id, course_id)
        return response
    else:  # In production, we use RQ
        current_app.task_queue.enqueue_call(
            func=tw_api_utils.add_family_with_child,
            args=(payload_child, payload_family, crm_id, course_id),
            result_ttl=5000,
        )
        return "Success!"


@teachworks.route("/add_independent", methods=["POST"])
@authenticate(admin_auth)
@body(TeachworksIndependentSchema)
@other_responses({401: 'Bad request: error in body.'})
def add_independent(user):
    """ Adds an independent student to TW."""
    data = request.json

    students_attributes = {
        "calender_color": "#0A61F7",
        "billing_method": "Package",
        "welcome_email": True,
        "enable_user_account": True,
        "email_lesson_reminders": True,
        "email_lesson_notes": True,
    }

    # Optional fields
    if "default_location_id" in data:
        students_attributes["default_location_id"] = data["default_location_id"]

    if "default_service_ids" in data:
        students_attributes["default_service_ids"] = data["default_service_ids"]

    if "default_teacher_ids" in data:
        students_attributes["default_teacher_ids"] = data["default_teacher_ids"]

    payload = {
        "customer": {
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "email": data["email"],
            "mobile_phone": data["mobile_phone"],
            "status": "Active",
            "welcome_email": True,
            "enable_user_account": True,
            "students_attributes": [
                students_attributes
            ]
        }
    }

    if "course_id" in request.json:
        course_id = request.json["course_id"]
    else:
        course_id = None

    if "crm_id" in request.json:
        crm_id = request.json["crm_id"]
    else:
        crm_id = None

    if config("CONFIG_NAME") == "production":
        current_app.task_queue.enqueue_call(
            func=tw_api_utils.add_independent,
            args=(payload, crm_id, course_id),
            result_ttl=5000,
        )
        return "Success!"
    else:
        response = tw_api_utils.add_independent(payload, crm_id, course_id)
        return response
