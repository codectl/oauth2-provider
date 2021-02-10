import os


class BaseConfig:
    DEBUG = False
    TESTING = False

    # Name of the host
    HOST = os.getenv('FLASK_RUN_HOST', '0.0.0.0')

    # Application root for the Web application
    APP_ROOT = '/api'

    # Database settings
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_CONNECT_OPTIONS = {}

    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2

    # Session secret
    SECRET_KEY = os.getenv('SECRET_KEY')

    # Additional settings

    TOKEN_ENDPOINT_AUTH_METHODS = [
        'client_secret_basic',
        'client_secret_post',
        'none',
    ]

    # don't use session to keep the value of 'next'.
    # Instead the the value is kept on the url.
    USE_SESSION_FOR_NEXT = bool(os.getenv('USE_SESSION_FOR_NEXT', False))

    # include refresh token when issuing an access token.
    OAUTH2_REFRESH_TOKEN_GENERATOR = bool(os.getenv('OAUTH2_REFRESH_TOKEN_GENERATOR', False))

    # include a new refresh token when refreshing an access token
    INCLUDE_NEW_REFRESH_TOKEN = bool(os.getenv('INCLUDE_NEW_REFRESH_TOKEN', False))


class ProductionConfig(BaseConfig):
    ENV = os.getenv('FLASK_ENV', 'production')
    PORT = os.getenv('FLASK_RUN_PORT', 5000)
    LOG_LEVEL = 'INFO'


class DevelopmentConfig(BaseConfig):
    ENV = os.getenv('FLASK_ENV', 'development')
    PORT = os.getenv('FLASK_RUN_PORT', 5001)
    DEBUG = True
    LOG_LEVEL = 'DEBUG'


class TestingConfig(BaseConfig):
    ENV = os.getenv('FLASK_ENV', 'test')
    PORT = os.getenv('FLASK_RUN_PORT', 5002)
    TESTING = True
    LOG_LEVEL = 'DEBUG'


config_by_name = dict(
    production=ProductionConfig,
    development=DevelopmentConfig,
    testing=TestingConfig
)
