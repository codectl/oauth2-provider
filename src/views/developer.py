import time

from flask import Blueprint, current_app, redirect, render_template, request, url_for
from flask_login import current_user
from werkzeug.security import gen_salt

from src import db
from src.models.OAuth2Client import OAuth2Client
from src.views import roles_required

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
        client_id = gen_salt(24)
        client_id_issued_at = int(time.time())
        client = OAuth2Client(
            client_id=client_id,
            client_id_issued_at=client_id_issued_at,
            resource_owner_id=current_user.id,
        )

        form = request.form
        client_metadata = {
            "client_name": form["client_name"],
            "client_uri": form["client_uri"],
            "grant_types": split_by_crlf(form["grant_type"]),
            "redirect_uris": split_by_crlf(form["redirect_uri"]),
            "response_types": split_by_crlf(form["response_type"]),
            "scope": form["scope"],
            "token_endpoint_auth_method": form["token_endpoint_auth_method"]
        }
        client.set_client_metadata(client_metadata)

        if form['token_endpoint_auth_method'] == 'none':
            client.client_secret = ''
        else:
            client.client_secret = gen_salt(48)

        db.session.add(client)
        db.session.commit()

        current_app.logger.info(
            "Registered new client application...\n"
            "Client Id: {0}\n"
            "Resource Owner: '{1}'\n"
            "Additional data: {2}".format(
                client_id,
                current_user.username,
                client_metadata)
        )

        return redirect(url_for('developer.me_route'))
    else:
        clients = OAuth2Client.query.filter_by(resource_owner_id=current_user.id).all()

        return render_template('pages/developer/clients.html', clients=clients)


def split_by_crlf(s):
    return [v for v in s.splitlines() if v]
