import requests
import json


def is_human(captcha_response, captcha_secret):
    """ Validating recaptcha response from google server
        Returns True captcha test passed for submitted form else returns False.
    """
    payload = {'response': captcha_response, 'secret': captcha_secret}
    response = requests.post(
        "https://www.google.com/recaptcha/api/siteverify", payload)

    response_text = json.loads(response.text)
    # print(response_text['score'])
    if response_text['success'] is True and response_text['score'] > 0.5:
        return True
    return False
