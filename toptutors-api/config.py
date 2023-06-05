import os
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


def as_bool(value):
    if value:
        return value.lower() in ['true', 'yes', 'on', '1']
    return False


sqlalchemy_pool_size = os.environ.get("SQLALCHEMY_POOL_SIZE") or 4
sqlalchemy_max_overflow = os.environ.get("SQLALCHEMY_MAX_OVERFLOW") or 3


class Config(object):
    # database options
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RQ_DASHBOARD_REDIS_URL = os.environ.get("REDIS_URL")
    # security options
    SECRET_KEY = os.environ.get('SECRET_KEY_CONFIG', 'top-secret!')
    DEBUG = False
    TESTING = False
    JSON_AS_ASCII = False
    LESSON_SPACE_API_KEY = os.environ.get('LESSON_SPACE_API_KEY')
    LESSON_SPACE_ORGANIZATION = os.environ.get('LESSON_SPACE_ORGANIZATION')
    DISABLE_AUTH = as_bool(os.environ.get('DISABLE_AUTH'))
    ACCESS_TOKEN_MINUTES = int(os.environ.get('ACCESS_TOKEN_MINUTES') or '1')
    REFRESH_TOKEN_DAYS = int(os.environ.get('REFRESH_TOKEN_DAYS') or '90')
    REFRESH_TOKEN_IN_COOKIE = as_bool(os.environ.get(
        'REFRESH_TOKEN_IN_COOKIE') or 'yes')
    REFRESH_TOKEN_IN_BODY = as_bool(os.environ.get('REFRESH_TOKEN_IN_BODY'))
    RESET_TOKEN_MINUTES = int(os.environ.get('RESET_TOKEN_MINUTES') or '60')
    PASSWORD_RESET_URL = os.environ.get('PASSWORD_RESET_URL') or \
        'http://localhost:3000/reset'
    CONFIRMATION_URL = os.environ.get('CONFIRMATION_URL') or \
        'https://localhost:3000/auth/confirmation'
    USE_CORS = as_bool(os.environ.get('USE_CORS') or 'yes')
    CORS_SUPPORTS_CREDENTIALS = True
    CAPTCHA_SITE_KEY = os.environ.get('CAPTCHA_SITE_KEY')
    CAPTCHA_SECRET_KEY = os.environ.get('CAPTCHA_SECRET_KEY')

    # Services
    OPENAI = os.environ.get('OPENAI')
    ZOHO_ADD_STRIPE_ID_TO_DEAL = os.environ.get('ZOHO_ADD_STRIPE_ID_TO_DEAL')
    ZOHO_ADD_TASK_ERROR = os.environ.get('ZOHO_ADD_TASK_ERROR')
    ZOHO_PACKAGE_PAID = os.environ.get('ZOHO_PACKAGE_PAID')

    # API documentation
    APIFAIRY_TITLE = 'TopTutors Old  API'
    APIFAIRY_VERSION = ''
    APIFAIRY_UI = os.environ.get('DOCS_UI', 'elements')
    APIFAIRY_UI_PATH = "/admin/docs"

    # email options
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'localhost')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or '25')
    MAIL_USE_TLS = as_bool(os.environ.get('MAIL_USE_TLS'))
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get(
        'AWS_SES_SENDER',
        'donotreply@toptutors.dk'
    )


class DevelopmentConfig(Config):
    ENV_NAME = "development"
    DEBUG = True
    # DEVELOPMENT DATABASE
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "SQLALCHEMY_DATABASE_URI_TEST_PORTAL")
    SQLALCHEMY_ECHO = as_bool(os.environ.get('SQLALCHEMY_ECHO') or "false")
    #SQLALCHEMY_ENGINE_OPTIONS = {"pool_size": int(sqlalchemy_pool_size),
    #                            "max_overflow": int(sqlalchemy_max_overflow)}

class ProductionConfig(Config):
    ENV_NAME = "production"
    #SQLALCHEMY_ENGINE_OPTIONS = {"pool_size": int(sqlalchemy_pool_size),
    #                             "max_overflow": int(sqlalchemy_max_overflow)}
    # PRODUCTION DATABASE
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")


class TestingConfig(Config):
    ENV_NAME = "testing"
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "SQLALCHEMY_LOCAL_TEST") + os.path.join(basedir, 'database.db')
    #SQLALCHEMY_ENGINE_OPTIONS = {"pool_size": None,
    #                             "max_overflow": None}

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
