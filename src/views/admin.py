from flask import Blueprint, render_template

from src.models.OAuth2Client import OAuth2Client
from src.services.user import UserService

admin = Blueprint(__name__, 'admin')


@admin.route('/', methods=('GET', 'POST'))
def index():
    user = UserService.current_user()

    if 'admin' not in user.roles:
        return render_template('error.html'), 201

    if user:
        clients = OAuth2Client.query.filter_by(user_id=user.id).all()
    else:
        clients = []

    return render_template('admin.html', user=user, clients=clients)
