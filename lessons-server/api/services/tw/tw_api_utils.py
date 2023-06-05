import requests
import json

from time import sleep

from api.app import db
from api.services.zoho_crm import update_teachworks_id, error_notification_to_zoho
from models.course import Course
from api.services.tw.tw_headers import tw_headers


def get_tutor_list():
    """Gets the all the tutors from TW API
    returns: a list of tutors
    rtype: List
    """
    payload = {}
    tutor_list = []

    # We create a counter and a exit variable
    # this is needed, since the TW API has their data,
    # seperated in multiple pages - 20 employees pr page,
    # so we need to loop through all the pages and get all employees
    still_data = True
    counter = 1

    # While there are more pages of data
    while still_data:
        response = requests.request(
            "GET",
            "https://api.teachworks.com/v1/employees",
            headers=tw_headers,
            data=payload,
            params={"page": str(counter), "per_page": 50},
        )
        counter += 1
        tutor_list.extend(response.json())
        # If the response is empty, there are no more pages,
        # and we can break the loop
        if not response.json():
            still_data = False
        else:
            sleep(0.5)
    # pp(tutor_list)
    return tutor_list


def get_subjects():
    payload = {}
    subjects = []

    still_data = True
    counter = 1

    while still_data:
        response = requests.request(
            "GET",
            "https://api.teachworks.com/v1/subjects",
            headers=tw_headers,
            data=payload,
            params={"page": str(counter), "per_page": 50}
        )
        counter += 1
        subjects.extend(response.json())

        if not response.json():
            still_data = False
        else:
            sleep(0.5)
    return subjects


def add_family_with_child(payload_child, payload_family, crm_id=None, course_id=None):
    """ Things that could go wrong and might have to be optimized for in the future: 1. found active customer is not parent type. 2. Student email already exists as account. """
    response_family = requests.post(
        "https://api.teachworks.com/v1/customers/family", headers=tw_headers, json=payload_family)
    sleep(0.5)

    if response_family.status_code == 400:
        error_notification_to_zoho("Account already existed on TW.",
                                   f"Email already exists. {payload_family} with child {payload_child}. TW Response: {response_family.content}", crm_id)
        # Current TW Customer or student already exists with this email.
        if "Email has already been taken as a username." in response_family.json()["errors"][0]:
            # Get all customers with said email.
            customers_result = get_to_tw(
                "customers", {"email": payload_family["email"]})
            # print(customers_result, "customer result")
            # If there's only one result then let's use this old profile instead.
            if len(customers_result) == 1:
                # Let's just double check that the profile is active.
                if customers_result[0]["status"] != "Active":
                    # It's not active, so let's activate it.
                    payload = {"customer": {"status": "Active"}}
                    put_to_tw(
                        f"customers/{customers_result[0]['id']}", payload)

                # We will use this profile as the family profile.
                tw_customer_id = customers_result[0]["id"]
            else:  # if there are multiple results with said email.
                # Let's only get the active customers (if there are any)
                active_customers = [customer for customer in customers_result if customer["status"] ==
                                    "Active" and customer["customer_type"] == "family" and customer["welcome_sent_at"] is not None]
                # If there's 1 active profile then let's use this profile
                if len(active_customers) == 1:
                    tw_customer_id = active_customers[0]["id"]
                # If there's more than 1 active profile then let's use the first one.
                elif len(active_customers) > 1:
                    tw_customer_id = active_customers[0]["id"]
                # If there are no active profiles and multiple inactive ones then we make the first one active again.
                else:
                    # This is probably because the account created is not a family account, but an independent student or child.
                    if crm_id is None:
                        crm_id = 0
                    error_notification_to_zoho(
                        "Could not create family account, because account already exists with this mail.",
                        f"Email already exists. {payload_family} with child {payload_child}. TW Response: {response_family.content}",
                        crm_id)
    else:
        tw_customer_id = response_family.json()["id"]

    payload_child["customer_id"] = tw_customer_id

    response_child = requests.post(
        "https://api.teachworks.com/v1/students", headers=tw_headers, json=payload_child)
    # print(response_family.json(), " CUSTOMER data")
    # print(tw_customer_id, " TW CUSTOMER ID")
    # print(response_child.json())
    tw_student_id = response_child.json()["id"]

    # Updates TW ID in CRM Deal
    if crm_id is not None:
        update_teachworks_id(tw_customer_id, crm_id)

    # Updates TW ID in DB Course Table
    if course_id is not None:
        Course.update_tw_id(course_id, tw_customer_id, tw_student_id)

    return response_child.json()


def add_independent(payload_student: dict, crm_id: int = None, course_id=None):
    """ Adds an independent student to TW.
    If CRM_ID is not None then we update the CRM Deal with the Teachworks link.
    If course_id is not None then we update the Course Table in DB with the customer/student TW id.
    """
    response = requests.post(
        "https://api.teachworks.com/v1/customers/independent_student", headers=tw_headers, json=payload_student)
    sleep(0.5)

    # print(response.json())
    if response.status_code == 400:
        if "Email has already been taken as a username." in response.json()["errors"][0]:
            # Get all customers with said email.
            customers_result = get_to_tw(
                "customers", {"email": payload_student["customer"]["email"]})
            # print(customers_result, "customer result")
            # If there's only one result then let's use this old profile instead.
            if len(customers_result) == 1:
                # Let's just double check that the profile is active.
                if customers_result[0]["status"] != "Active":
                    # It's not active, so let's activate it.
                    payload = {"customer": {"status": "Active"}}
                    put_to_tw(
                        f"customers/{customers_result[0]['id']}", payload)

                # We will use this profile as the family profile.
                tw_customer_id = customers_result[0]["id"]
            else:  # if there are multiple results with said email.
                # Let's only get the active customers (if there are any)
                active_customers = [
                    customer for customer in customers_result if customer["status"] == "Active"
                    and customer["customer_type"] == "independent"
                    and customer["welcome_sent_at"] is not None]
                # If there's 1 active profile then let's use this profile
                if len(active_customers) == 1:
                    tw_customer_id = active_customers[0]["id"]
                # If there's more than 1 active profile then let's use the first one.
                elif len(active_customers) > 1:
                    tw_customer_id = active_customers[0]["id"]
                # If there are no active profiles and multiple inactive ones then we make the first one active again.
                else:
                    # This is probably because the account created is not an independent account, but a family or child account.
                    if crm_id is None:
                        crm_id = 0
                    error_notification_to_zoho(
                        "Could not create independent account, because account already exists with this mail.", f"Email already exists. {payload}", crm_id)
    else:
        tw_customer_id = response.json()["id"]

    # Updates TW ID in CRM Deal
    if crm_id is not None:
        update_teachworks_id(tw_customer_id=tw_customer_id, crm_deal_id=crm_id)

    # Updates TW ID in DB Course Table
    if course_id is not None:
        Course.update_tw_id(course_id, tw_customer_id,
                            tw_customer_id)
    return response.json()


def add_to_tw(link, payload):
    """ This is the dynamic POST request to TW that depends on what endpoint you want to use."""
    response = requests.post(
        f"https://api.teachworks.com/v1/{link}", headers=tw_headers, json=payload)
    return response.json()


def put_to_tw(link, payload):
    """ This is the dynamic PUT request to TW that depends on what endpoint you want to use."""
    print(f"https://api.teachworks.com/v1/{link}")
    response = requests.put(
        f"https://api.teachworks.com/v1/{link}", headers=tw_headers, json=payload)
    sleep(0.5)
    return response.json()


def get_to_tw(link, payload):
    """ This is the dynamic GET request to TW that depends on what endpoint you want to use."""
    response = requests.get(
        f"https://api.teachworks.com/v1/{link}", headers=tw_headers, json=payload)
    return response.json()


def get_lessons():
    """Get all lessons"""

    payload = {}
    lessons = []

    still_data = True
    counter = 1

    while still_data:
        response = requests.request(
            "GET",
            "https://api.teachworks.com/v1/lessons",
            headers=tw_headers,
            data=payload,
            params={"page": str(counter), "per_page": 50}
        )
        counter += 1
        lessons.extend(response.json())

        if not response.json():
            still_data = False
        else:
            sleep(0.5)
    return lessons


def get_tutor_students():
    """Get all the tutors current students.
    Returns list of dictionaries with tutor data from TW."""

    payload = {}
    students = []

    still_data = True
    counter = 1

    while still_data:
        response = requests.request(
            "GET",
            "https://api.teachworks.com/v1/students",
            headers=tw_headers,
            data=payload,
            params={"page": str(counter), "per_page": 50, "status": 'Active'}
        )
        counter += 1
        students.extend(response.json())

        if not response.json():
            still_data = False
        else:
            sleep(0.5)

    return students


def add_student(name, email, mobile_phone, additional_notes, zip_code):
    """Adds a student to TW's Prospective student section
    param name: str
    param email: str
    param mobile_phone: str
    param additional_notes: str
    param zip_code: int
    """

    # Check if there is more than 1 substring in the string
    if len(name.split()) > 1:
        # We split the name to 2 strings, after the first space
        first_name = name.split()[0]
        last_name = name.split()[1]
    else:
        # Set first name, and last name to "."
        first_name = name
        last_name = "."

    # The data we send through the POST request
    # HAS to send billing method or we get 400 - bad request
    # Dont know why, guess the API is just that way ...
    data = {
        "customer": {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "mobile_phone": mobile_phone,
            "status": "Prospective",
            "additional_notes": additional_notes,
            "zip": zip_code,
            "students_attributes": [{
                "billing_method": "Package",
                "email_lesson_reminders": True,
            }],
        }
    }

    requests.post(
        "https://api.teachworks.com/v1/customers/independent_student",
        headers=tw_headers,
        data=json.dumps(data),
    )


if __name__ == "__main__":
    # get_tutor_list()
    pass
