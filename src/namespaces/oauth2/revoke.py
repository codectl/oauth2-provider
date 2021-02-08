from flask_restplus import Resource

from src.oauth2 import authorization


class Revoke(Resource):

    @staticmethod
    def post():
        return authorization.create_endpoint_response('revocation')
