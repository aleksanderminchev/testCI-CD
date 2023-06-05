import requests
import jwt

from datetime import datetime as date
from decouple import config


def create_ghost_auth_token():
    """ Creates a ghost CMS blog authentication token. """
    api_key = config("GHOST_API")
    # Split the key into ID and SECRET
    id, secret = api_key.split(':')

    # Prepare header and payload
    iat = int(date.now().timestamp())

    header = {'alg': 'HS256', 'typ': 'JWT', 'kid': id}
    payload = {
        'iat': iat,
        'exp': iat + 5 * 60,
        'aud': '/admin/'
    }
    token = jwt.encode(payload, bytes.fromhex(secret), algorithm='HS256', headers=header)
    return token


def request_with_token(token: str, method: str, url: str, body: dict):
    headers = {'Authorization': f'Ghost {token}'}
    response = requests.request(method, url, json=body, headers=headers)
    return response


def request_without_token(method: str, url: str, body: dict):
    """ Choose REST method, endpoint, and body data. """
    token = create_ghost_auth_token()
    return request_with_token(token, method, url, body)
