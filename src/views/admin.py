from flask import Blueprint, render_template

from src.views import roles_required

admin = Blueprint('admin', __name__)


@admin.before_request
@roles_required('Admin')
def before_request():
    """
    For each request, check whether user has Admin role.
    """
    print(2)


@admin.route('/', methods=('GET', 'POST'))
def index():
    print(1)
    return render_template('pages/admin/index.html')
