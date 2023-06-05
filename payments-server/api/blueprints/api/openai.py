import json

from flask import Blueprint
from apifairy import authenticate, body
from apifairy.decorators import other_responses

from api.schemas import OpenaiSchema, DalleSchema
from api.auth import admin_auth
from api.services.openai_api import openAICompletion

openai = Blueprint('openai', __name__)


@openai.route('/completion', methods=['POST'])
@authenticate(admin_auth)
@body(OpenaiSchema)
@other_responses({404: 'Invalid request'})
def query(args):
    """ Creates an OpenAI Query.

    Optional fields and default values:
    temperature: int = 1,
    max_tokens: int = 50,
    n: int = 1
    """
    user = admin_auth.current_user()
    user_id = str(user.uid)
    output = openAICompletion(user=user_id, **args)

    if 'choices' in output and len(output['choices']) > 0:
        answer = json.loads(str(output))
    else:
        answer = 'Opps sorry, you beat the AI this time'
    return answer


@openai.route('/image', methods=['POST'])
@authenticate(admin_auth)
@body(DalleSchema)
@other_responses({404: 'Invalid request'})
def dalle_query(args):
    """ Creates an OpenAI Dall-E Query.

    Optional fields and default values:
    n: int = 1
    """
    user = admin_auth.current_user()
    user_id = str(user.uid)
    output = openAICompletion(user=user_id, **args)

    if 'choices' in output and len(output['choices']) > 0:
        answer = json.loads(str(output))
    else:
        answer = 'Opps sorry, you beat the AI this time'
    return answer
