from flask import render_template, redirect, request, url_for
from flask_login import current_user
from flask_restplus import Resource


class Authorize(Resource):

    def get(self):
        """
        Granting client authorization for corresponding scopes.
        """
        return redirect(url_for('auth.authorize_route', **request.args))

    # def post(self):
    #     confirmed = request.form['confirm']
    #     if confirmed:
    #         # Granted by resource owner
    #         return authorization.create_authorization_response(grant_user=current_user)
    #
    #     # Denied by resource owner
    #     return authorization.create_authorization_response(grant_user=None)
