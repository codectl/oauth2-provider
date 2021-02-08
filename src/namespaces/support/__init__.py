from flask_restplus import Namespace

from .callback import ClientCallback
from .client import Client

support_namespace = Namespace('support', description='Verify the status of running components.')
support_namespace.add_resource(Client, '/client')
support_namespace.add_resource(ClientCallback, '/client/callback')
