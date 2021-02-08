from flask import request
from flask_restplus import Resource


class ClientCallback(Resource):
    """
    Callback endpoint for the server side test client.
    """

    def get(self):
        return request.args
