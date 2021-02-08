from flask import render_template, redirect, request, url_for
from flask_login import current_user
from flask_restplus import Resource

from src.oauth2 import authorization


class Authorize(Resource):

    def get(self):
        # Login is required since we need to know the current resource owner.
        if current_user:
            grant = authorization.validate_consent_request(end_user=current_user)
            return render_template(
                'pages/auth/authorize.html',
                grant=grant,
            )
        else:
            return redirect(url_for('auth.login_route'))

    def post(self):
        confirmed = request.form['confirm']
        if confirmed:
            # Granted by resource owner
            return authorization.create_authorization_response(grant_user=current_user)

        # Denied by resource owner
        return authorization.create_authorization_response(grant_user=None)
