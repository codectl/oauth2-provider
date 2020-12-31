import time

from flask import Blueprint, redirect, render_template, request
from werkzeug.security import gen_salt

from src import db
from src.models.OAuth2Client import OAuth2Client
from src.services.user import UserService

developer = Blueprint('developer', __name__)


@developer.route('/me', methods=('GET', 'POST'))
def index():
    user = UserService.current_user()

    clients = OAuth2Client.query.filter_by(user_id=user.id).all()

    return render_template('pages/developer/index.html', user=user, clients=clients)


@developer.route('/me/clients', methods=['POST'])
def client_application():
    user = UserService.current_user()

    if not user:
        return redirect('/')

    client_id = gen_salt(24)
    client_id_issued_at = int(time.time())
    client = OAuth2Client(
        client_id=client_id,
        client_id_issued_at=client_id_issued_at,
        resource_owner_id=user.id,
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
    return redirect('/')


def split_by_crlf(s):
    return [v for v in s.splitlines() if v]
