import requests
from api.services.tw.tw_headers import tw_headers


def get_students(email):
    """ Get students by email. Returns a list of students dicts containing their TW information. """
    payload = {}
    response = requests.request(
        "GET",
        "https://api.teachworks.com/v1/students",
        headers=tw_headers,
        data=payload,
        params={"email": email, "direction": "desc"},
    )
    return response.json()
