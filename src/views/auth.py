from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user

from src import login_manager
from src.services.user import UserService

auth = Blueprint('auth', __name__)


def login_not_required(f):
    """
    Decorator for endpoints that do not require login
    """

    f.login_not_required = True
    return f


@login_manager.user_loader
def load_user(user_id):
    return UserService.get(user_id)


@auth.route('/')
@login_not_required
def index():
    return redirect(url_for('auth.login'))


@auth.route('/login', methods=('GET', 'POST'))
@login_not_required
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not UserService.authenticate(username, password):
            flash('Invalid user key or password. Please try again.', 'danger')
            current_app.logger.warn("Invalid credentials attempted for username '{0}'.".format(username))

            return redirect(url_for('auth.login'))

        # Find or create user
        user = UserService.find_by(username=username, fetch_one=True)
        if user:
            UserService.update(user.id, authenticated=True)
        else:
            user = UserService.create(username=username, authenticated=True)

        # Log in user in Flask
        login_user(user)

        # Go to next page if defined
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)

        return redirect(url_for('user.me'))
    else:
        return render_template('pages/auth/authenticate.html')


def resource_authorization():
    """
    Redirect user to login if user has no active session.
    """

    if not current_user.is_authenticated:
        view = current_app.view_functions[request.endpoint]
        if not getattr(view, 'login_not_required', False):
            return current_app.login_manager.unauthorized()
