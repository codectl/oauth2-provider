from flask import Blueprint, render_template

from src.views import roles_required

admin = Blueprint('admin', __name__)


@admin.before_request
@roles_required('Admin')
def before_request():
    """
    For each request, check whether user has Admin role.
    """
    pass


@admin.route('/', methods=('GET', 'POST'))
def index():
    return render_template('pages/admin/index.html')
