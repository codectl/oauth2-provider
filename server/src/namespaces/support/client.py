from flask_restplus import fields, Resource

from server.src.views.api import api
from server.src.services.oauth2.client import OAuth2ClientService
from server.src.services.user import UserService


model = api.model('Client', {
    'client_id': fields.String,
    'client_secret': fields.String,
    'resource_owner': {
        'username': fields.String(attribute='resource_owner.username'),
    },
    'issued_at': fields.Integer(attribute='client_id_issued_at'),
    'secret_expires_at': fields.Integer(attribute='client_secret_expires_at'),
    'metadata': fields.Raw(attribute='client_metadata')
})


class Client(Resource):
    """
    A server side client used for testing OAuth2 requests.
    """

    def get(self):
        """
        Get the dummy client for testing purposes.
        """
        client = OAuth2ClientService.find_by(resource_owner_id=UserService.find_by(username='admin', fetch_one=True).id,
                                             fetch_one=True)
        return client.client_info
