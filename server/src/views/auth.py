from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for, session
from flask_login import current_user, login_user

from server.src import login_manager
from server.src.oauth2 import authorization
from server.src.services.user import UserService

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
def index_route():
    return redirect(url_for('auth.login_route'))


@auth.route('/login', methods=('GET', 'POST'))
@login_not_required
def login_route():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not UserService.authenticate(username, password):
            flash('Invalid user key or password. Please try again.', 'danger')
            current_app.logger.warn("Invalid credentials attempted for username '{0}'.".format(username))

            return redirect(url_for('auth.login_route'))

        # Find or create user
        user = UserService.find_by(username=username, fetch_one=True)
        if user:
            UserService.update(user.id, authenticated=True)
        else:
            user = UserService.create(username=username, authenticated=True)

        # Log in user in Flask
        login_user(user)

        # Go to next page if defined
        next_page = session.pop('next') or request.args.get('next')
        if next_page:
            return redirect(next_page)

        return redirect(url_for('auth.login_route'))
    else:
        if current_user.is_authenticated:
            return redirect(url_for('user.me_route'))
        else:
            return render_template('pages/auth/authenticate.html')


@auth.route('/authorize', methods=('GET', 'POST'))
def authorize_route():
    if request.method == 'POST':
        grant_user = current_user if request.form.get('confirm') else None
        return authorization.create_authorization_response(grant_user=grant_user)
    else:
        if current_user:
            grant = authorization.validate_consent_request(request=request, end_user=current_user)
            if grant.request.scope:
                return render_template('pages/auth/authorize.html', grant=grant)
            else:
                return authorization.create_authorization_response(grant_user=current_user)
        else:
            return redirect(url_for('auth.login_route'))


def resource_authorization():
    """
    Redirect user to login if user has no active session.
    """

    if request.endpoint:
        if request.endpoint.startswith('api'):
            # TODO some validation?
            pass
        else:
            view = current_app.view_functions[request.endpoint]
            if not getattr(view, 'login_not_required', False) and not current_user.is_authenticated:
                return current_app.login_manager.unauthorized()
