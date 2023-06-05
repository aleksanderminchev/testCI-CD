import requests
import json
import time
import hashlib
from decouple import config

access_token = config('META_ACCESS_CODE')
pixel_id = config('META_PIXEL_ID')


def hash_data(data: str):
    """ Hashes inputs to SHA256. """
    # Convert the phone number to bytes
    data_in_bytes = data.encode('utf-8')

    # Create a new SHA256 hash object
    hash_object = hashlib.sha256()

    # Update the hash object with the phone number
    hash_object.update(data_in_bytes)

    # Get the hexadecimal representation of the hash
    hash_hex = hash_object.hexdigest()

    return hash_hex


def add_event(event_name: str,  user_data: dict, external_id: str, test: bool = False):
    """ Adds a lead event to Meta Pixel through CAPI.
    """

    user_data["external_id"] = hash_data(external_id)

    # Hash the email
    if "em" in user_data:
        user_data["em"] = hash_data(user_data["em"])

    # Hash the first name
    if "fn" in user_data:
        user_data["fn"] = hash_data(user_data["fn"])

    # Format and hash the phone number
    if "ph" in user_data:
        number = user_data["ph"][0]
        if number[0] == '+':
            # Remove the country code from the phone number
            user_data["ph"] = [hash_data(number[1:])]
        elif number[:2] == '00':
            # Remove the country code from the phone number
            user_data["ph"] = [hash_data(number[2:])]
        else:
            # Add the country code to the phone number
            user_data["ph"] = [hash_data("45" + number)]

    data = {
        "data": [
            {
                "event_name": event_name,
                "event_time": int(time.time()),
                "action_source": "website",
                "user_data": user_data
            }
        ],
        "access_token": access_token

    }
    if test:
        data["test_event_code"] = "TEST62246"

    payload = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    url = f"https://graph.facebook.com/v15.0/{pixel_id}/events"
    response = requests.request("POST", url, headers=headers, data=payload)
    if "error" in response.json():
        raise Exception(f"Request to Meta Failed: {response.content}")
