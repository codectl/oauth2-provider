from flask_restplus import Resource

from server.src.oauth2 import authorization


class Revoke(Resource):

    @staticmethod
    def post():
        return authorization.create_endpoint_response('revocation')
