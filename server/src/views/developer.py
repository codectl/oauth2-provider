from flask import Blueprint, current_app, redirect, render_template, request, url_for
from flask_login import current_user

from server.src.views import roles_required
from server.src.services.oauth2.client import OAuth2ClientService

developer = Blueprint('developer', __name__)


@developer.before_request
@roles_required('Developer')
def before_request():
    """
    For each request, check whether user has Developer role.
    """
    pass


@developer.route('/')
def index_route():
    return redirect(url_for('developer.me_route'))


@developer.route('/me', methods=('GET', 'POST'))
def me_route():
    return render_template('pages/developer/index.html')


@developer.route('/me/clients', methods=('GET', 'POST'))
def clients_route():
    if request.method == 'POST':
        form = request.form
        client_metadata = {
            'client_name': form['client_name'],
            'client_uri': form['client_uri'],
            'grant_types': form['grant_type'].splitplines(),
            'redirect_uris': form['redirect_uri'].splitplines(),
            'response_types': form['response_type'].splitplines(),
            'scope': form['scope'],
            'token_endpoint_auth_method': form['token_endpoint_auth_method']
        }

        client = OAuth2ClientService.create(
            resource_owner_id=current_user.id,
            client_metadata=client_metadata
        )

        current_app.logger.info(
            "Registered new client application...\n"
            "Client Id: {0}\n"
            "Resource Owner: '{1}'\n"
            "Additional data: {2}".format(
                client.client_id,
                current_user.username,
                client_metadata)
        )

        return redirect(url_for('developer.me_route'))
    else:
        clients = OAuth2ClientService.find_by(resource_owner_id=current_user.id)

        return render_template('pages/developer/clients.html', clients=clients)
