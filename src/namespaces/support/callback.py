from flask import request
from flask_restplus import fields, marshal, Resource

from src.views.api import api
from src.services.oauth2.code import OAuth2AuthorizationCodeService


model = api.model('AuthorizationCode', {
    'code': fields.String,
    'client_id': fields.String,
    'redirect_uri': fields.String,
    'response_type': fields.String,
    'resource_owner': {
        'username': fields.String(attribute='resource_owner.username'),
    },
    'scope': fields.String,
    'auth_time': fields.Integer,
})


class ClientCallback(Resource):
    """
    Callback endpoint for the server side test client.
    """

    def get(self):
        return marshal(OAuth2AuthorizationCodeService.find_by(code=request.args.get('code'), fetch_one=True), model)
