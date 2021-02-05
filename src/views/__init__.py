from functools import wraps

from flask import abort
from flask_login import current_user


def roles_required(*role_names):
    """
    This decorator ensures that the current user
    has *all* of the specified roles (AND operation).

    Example::

        @route('/escape')
        @roles_required('Special', 'Agent')
        def escape_capture():  # User must be 'Special' AND 'Agent'
            ...

    Raises 403 when the user does not have the required roles.
    Calls the decorated view otherwise.
    """

    def wrapper(view_function):
        @wraps(view_function)
        def decorator(*args, **kwargs):
            print(current_user.roles)
            # User must have the required roles
            if not current_user.has_roles(*role_names):
                abort(403)

            return view_function(*args, **kwargs)

        return decorator

    return wrapper
