import os

from dotenv import load_dotenv
from flask import Flask, redirect

from src import db, login_manager
from src.namespaces.oauth2 import oauth2_namespace
from src.oauth2 import config_oauth
from src.settings.config import config_by_name
from src.views.api import api, restful_api
from src.views.admin import admin
from src.views.auth import auth, resource_authorization
from src.views.developer import developer
from src.views.user import user


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

    # Redirect root point to app context root
    app.add_url_rule('/', 'index', lambda: redirect(app.config['APP_ROOT']))

    # Initialize and configure OAuth2
    config_oauth(app)

    # Register blueprints
    app.register_blueprint(restful_api, url_prefix=app.config['APP_ROOT'])
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(developer, url_prefix='/developers')
    app.register_blueprint(user, url_prefix='/users')

    # ... and namespaces
    api.add_namespace(oauth2_namespace, path='/oauth2')

    # Additional configurations
    app.before_request_funcs[None] = [resource_authorization]
