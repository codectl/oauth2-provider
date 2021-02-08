from flask_restplus import Namespace, Resource

ns = Namespace('support', description='Verify the status of running components.')


@ns.route('/app')
class App(Resource):
    """
    A server side test app used for testing OAuth2 requests.
    """

    def get(self):
        return 200


@ns.route('/app/callback')
class AppCallback(Resource):
    """
    Callback endpoint for the server side test app.
    """

    def get(self):
        pass
