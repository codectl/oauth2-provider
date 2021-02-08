from flask_restplus import Resource


class Client(Resource):
    """
    A server side client used for testing OAuth2 requests.
    """

    def get(self):
        return 200
