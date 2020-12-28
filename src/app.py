import os

from dotenv import load_dotenv
from flask import Blueprint, Flask, redirect
from flask_restplus import Api

from src import db, login_manager
from src.namespaces.oauth2 import oauth2_namespace
from src.oauth2 import config_oauth
from src.settings.config import config_by_name
from src.views.admin import admin
from src.views.auth import auth, resource_authorization
from src.views.developer import developer


def create_app(config_name=None):
    """
    Create a new app.
    """

    # Define the WSGI application object
    app = Flask(__name__)

    # Load .env and variables
    load_dotenv()

    # Load object-based default configuration
    env = os.getenv('FLASK_ENV', config_name)
    app.config.from_object(config_by_name[env])

    setup_app(app)

    return app


def setup_app(app):
    """
    Setup the app
    """

    # Link db to app
    db.init_app(app)

    # LoginManager setup
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Create tables if they do not exist already
    with app.app_context():
        db.create_all()

    # Create API blueprint
    blueprint = Blueprint('api', __name__, url_prefix=app.config['APP_ROOT'])

    # Redirect root point to app context root
    app.add_url_rule('/', 'index', lambda: redirect(app.config['APP_ROOT']))

    # Initialize Flask Restplus root api
    api = Api(blueprint,
              title='OAuth2 Provider Service API',
              version='1.0',
              description='an OAuth2 service implementation to manage authorization requests.'
              )

    # Initialize and configure OAuth2
    config_oauth(app)

    # Register blueprints
    app.register_blueprint(blueprint)
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(developer, url_prefix='/developer')

    # ... and namespaces
    api.add_namespace(oauth2_namespace, path='/oauth2')

    # Additional configurations
    app.before_request_funcs[None] = [resource_authorization]
