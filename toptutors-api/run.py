from api import create_app
from decouple import config


app = create_app(config("CONFIG_NAME"))
