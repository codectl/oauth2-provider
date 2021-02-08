from flask import request
from flask_restplus import Resource

from src.oauth2 import authorization


class Token(Resource):

    @staticmethod
    def post():
        return authorization.create_token_response(request=request)
