import openai
from decouple import config

openai.api_key = config('OPENAI')


# submission = request.form['outline']
# prompt = f"Skriv en outline til et essay om {submission}:"
# openAIAnswerUnformatted = aicontent.openAIQuery(prompt)
# openAIAnswer = openAIAnswerUnformatted.replace('\n', '<br>')
# prompt = 'AI Suggestions for {} are:'.format(submission)


def openAICompletion(prompt: str, user: str, temperature: int = 1, max_tokens: int = 50, n: int = 1):
    """ Creates an OpenAI completion request. """
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        user=user,
        n=n
    )
    return response


def openAIImage(prompt: str, user: str = "admin", n: int = 1):
    """ Creates an Dall-e image creation request. """
    response = openai.Image.create(
        prompt=prompt,
        n=n,
        size="1024x1024",
        response_format="url",
        user=user
    )
    return response
