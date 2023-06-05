import requests

from decouple import config
from api.services import stripe_api
from api.services.tw import students
from models.tutor import Tutor


def add_contact_and_deal(
    name,
    email,
    phone,
    zip_code,
    num_people,
    help_types,
    education,
    course_subject,
    online_session,
    note,
    school_level,
    lead_type,
):
    """Adds a student as a contact and then adds a deal belonging to that student.
    Returns False on error and True on success"""

    if note is None:
        note = ""

    # get TW profile id if we have the email
    if email != "":
        try:  # try finding the TW user id
            tw_students = students.get_students(email)
            tw_id = tw_students[0][
                "customer_id"
            ]  # only taking the id for the newest if there are multiple.
        except Exception:
            tw_id = ""

        try:  # try finding stripe user id
            stripe_id = stripe_api.get_customer_from_mail(email)["id"]
        except Exception:
            stripe_id = ""
    else:  # if mail does not exist we don't have a TW nor Stripe profile
        tw_id = ""
        stripe_id = ""

    city_name = ""
    municipality = ""

    # format the phone number properly
    if phone != "":
        if "+45" not in phone[:3] and "0045" not in phone[:4]:
            phone = "+45" + phone
        elif "0045" in phone[:4]:
            phone = "+45" + phone[4:]

    last_name = "."
    # if name is empty
    if name == "":
        first_name = ","
        last_name = "Ukendt"

    # Check if there is more than 1 substring in the string
    elif len(name.split()) > 1:
        # We split the name to 2 strings, after the first space
        first_name = name.split()[0]
        last_name = name.split()[1]

    else:  # if there is only a first name (no spaces)
        # Set first name, and last name to "."
        first_name = name

    # Format location to match with CRM
    if online_session == "online":
        location = "Online"
    elif online_session == "ligeglad":
        location = "Åben for begge"
    elif online_session == "fysisk":
        location = "Fysisk"
    else:
        location = ""

    if education is None:
        education = ""

    if school_level == "uni":
        school_level = "Universitet"
    elif school_level == "gym":
        school_level = "Gymnasium"
        course_subject = course_subject[2:].replace("gym_", "")
    elif school_level == "folke":
        school_level = "Folkeskole"
        education = education + " kl."
        course_subject = course_subject[2:].replace("folke_", "")
    else:
        school_level = ""
    if num_people is None:
        num_people = 1

    # store the types of course in a list e.g. exam help, homework help, and assignment help.
    course_types = []
    if help_types != []:
        if "lektie" in help_types:
            course_types.append("Lektiehjælp")
        if "eksamen" in help_types:
            course_types.append("Eksamenshjælp")
        if "afleveringer" in help_types:
            course_types.append("Afleveringshjælp")

    if lead_type == "Udfyldt tlf. nr. via hjemmesiden":
        title = "Phone lead (niveau, fag)"
        first_name = "Ukendt phone lead"
        last_name = "."
    else:
        title = str(name) + f" ({education}, {course_subject})"

    # only adding the TW link if we have it.
    if tw_id == "":
        tw_link = "https://toptutors.teachworks.com/"
    else:
        tw_link = f"https://toptutors.teachworks.com/customers/{str(tw_id)}"

    if stripe_id == "":
        stripe_link = "https://dashboard.stripe.com/"
    else:
        stripe_link = f"https://dashboard.stripe.com/customers/{str(stripe_id)}"

    if title == "" or title is None:
        title = "ukendt"

    if last_name == "" or last_name is None:
        last_name = "ukendt"

    params = {
        "first_name": first_name,
        "last_name": last_name,
        "phone": phone,
        "email": email,
        "city_name": city_name,
        "zip_code": zip_code,
        "tw_link": tw_link,
        "municipality": municipality,
        "title": title,
        "num_people": str(num_people),
        "location": location,
        "school_level": school_level,
        "education": education,
        "course_subject": course_subject,
        "note": note,
        "lead_type": lead_type,
        "stripe": stripe_link,
    }
    response = requests.post(config("ZOHO_ADD_LEAD_API"), params=params)
    return response.status_code
    # print(response)
    # print(response.content)


def tutor_accepted_course_webhook(course_tutor_id, course_crm_deal_id, tutor_email):
    params = {
        "tutor_tw_id": course_tutor_id,
        "crm_deal_id": course_crm_deal_id,
        "tutor_email": tutor_email,
    }
    response = requests.post(config("ZOHO_TUTOR_MATCHED_API"), params=params)
    return response.status_code


def update_teachworks_id(tw_customer_id: int, crm_deal_id: int):
    """ Sends request to CRM that updates TW ID. """
    response = requests.post(config("ZOHO_ADD_TW_ID_TO_DEAL"), params={
                             "tw_id": tw_customer_id, "crm_id": crm_deal_id})
    return response


def error_notification_to_zoho(error_title: str, error_message: str, deal_id: int = 0):
    response = requests.post(config("ZOHO_ERROR_DEAL"), params={
                             "deal_id": deal_id, "error_message": error_message, "error_title": error_title})
    return response
