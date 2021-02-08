from flask_restplus import Namespace

from .authorize import Authorize
from .revoke import Revoke
from .token import Token

oauth2_namespace = Namespace('oauth2', description='Authorization requests under OAuth2 specifications.')
oauth2_namespace.add_resource(Authorize, '/authorize')
oauth2_namespace.add_resource(Revoke, '/revoke')
oauth2_namespace.add_resource(Token, '/token')
