import time

from flask import Blueprint, redirect, render_template, request
from werkzeug.security import gen_salt

from src import db
from src.models.OAuth2Client import OAuth2Client
from src.services.user import UserService

admin = Blueprint(__name__, 'admin')


@admin.route('/', methods=('GET', 'POST'))
def admin_home():
    user = UserService.current_user()

    if 'admin' not in user.roles:
        return render_template('error.html'), 201

    if user:
        clients = OAuth2Client.query.filter_by(user_id=user.id).all()
    else:
        clients = []

    return render_template('admin.html', user=user, clients=clients)
