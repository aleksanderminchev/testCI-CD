# Use this to make requests to the lesson space API
# createa lesson space
# restrict who can enter
# get recordings
# embed recordings
from api import db
import jwt
import requests
from flask import current_app


def create_lesson_space(teacher, student):
    """ Save the secret key for each user
        Use the secret to sign the user data and create the url for them to connect with
        Save everything untill in the space_url in db user
        Add this into the schedule lesson
    """
    lesson_space_id = str(teacher.id) + "_" + str(student.id)
    # Make sure that Lessonspace ID is never more than 64 characters as this will lead to an error
    if len(lesson_space_id) > 64:
        lesson_space_id = lesson_space_id[:64]

    # lesson_url = lesson_space_url_call(lesson_space_id, teacher, 'teacher')
    lesson_url = lesson_space_url_call(lesson_space_id, student, 'student')
    return lesson_url


def lesson_space_url_call(lesson_space_id, user, type):
    api_key = current_app.config['LESSON_SPACE_API_KEY']

    response = requests.post(
        url='https://api.thelessonspace.com/v2/spaces/launch/',
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'Organisation ' + api_key
        },
        json={
            "id": lesson_space_id,
            "webhooks": {
                'session': {
                    'end': 'https://localhost:5000/api/redirect.'
                }
            }
        })

    json_result = response.json()
    url_for_db = ''
    url = json_result['client_url'].split('&')

    for i in url:
        if i[0:5] != 'user=':
            url_for_db = url_for_db + i + '&'

    return {"space": url_for_db, "secret": json_result["secret"], 'room_id': json_result['room_id'], 'session_id': json_result['session_id']}


def create_user_jwt_url(user, url, secret, type):
    if type == 'teacher':
        name = user.user.first_name + " " + user.user.last_name
        user_data = {
            "nbf": 0,
            "exp": 2147483647,
            "guest": False,
            "readOnly": False,
            "allowInvite": True,
            "id": 1513169,
            "canLead": True,
            'meta':
            {'name': name, 'profilePicture': ''}
        }
        encoded = jwt.encode(user_data, secret, algorithm="HS256")
        url = url + "user=" + encoded
        return url
    else:
        name = user.first_name + " " + user.last_name
        user_data = {
            "nbf": 0,
            "exp": 2147483647,
            "guest": False,
            "readOnly": False,
            "allowInvite": False,
            "id": 1513169,
            "canLead": True,
            'meta':
                {'name': name, 'profilePicture': ''}
        }

        encoded = jwt.encode(user_data, secret, algorithm="HS256")
        url = url + "user=" + encoded
        return url


def get_playback_url(teacher, student, session_id, lesson):
    lesson_space_id = str(teacher.id) + "_" + str(student.id)
    api_key = current_app.config['LESSON_SPACE_API_KEY']
    org_id = current_app.config['LESSON_SPACE_ORGANIZATION']
    response = requests.get(
        url='https://api.thelessonspace.com/v2/organisations/' +
            str(org_id) + '/sessions?search=' + session_id,
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'Organisation ' + api_key
        }
    )

    data = response.json()

    playback_object = {}
    print(lesson)
    print(data)
    print(data['results'])
    if len(data['results']) == 0:
        playback_object = {
            "name": lesson.title,
            "url": "",
            "start_time": lesson.from_time,
            "end_time": lesson.to_time
        }
    for i in data['results']:
        playback_object = {
            "name": i['name'],
            "url": i['playback_url'],
            "start_time": lesson.from_time,
            "end_time": lesson.to_time
        }

    return playback_object
