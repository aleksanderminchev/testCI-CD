import datetime
import time
import sys

from api.services.other_apis import is_human

from flask import request, current_app


class Updateable:
    def update(self, data):
        for attr, value in data.items():
            setattr(self, attr, value)
        return self


def get_date():
    """ gets current date """
    return datetime.datetime.utcnow()


def check_captcha(request: request):
    """ Returns boolean if it passes captcha or not. """
    try:
        captcha_response = request.form['g-recaptcha-response']
        captcha_secret = current_app.config["CAPTCHA_SECRET_KEY"]
        human = is_human(captcha_response, captcha_secret)
    except Exception:
        human = False
    return human


def create_payload(**data):
    payload = {}
    for key in data:
        payload[f"{key}"] = data[key]
    return payload


def measure_time_complexity(func, n):
    start_time = time.time()
    func()
    end_time = time.time()
    time_elapsed = end_time - start_time
    print(
        f"Time complexity of {func.__name__} for input size n={n}: {time_elapsed:.8f} seconds")


def measure_space_complexity(func, n):
    # Call the function with the input size n
    result = func(*n)

    # Get the size of the result object in bytes
    size = sys.getsizeof(result)

    # Print the space complexity in bytes
    print(
        f"Space complexity of {func.__name__} for input size n={n}: {size} bytes")
