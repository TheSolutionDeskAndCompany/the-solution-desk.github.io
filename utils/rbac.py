from functools import wraps
from flask_login import current_user
from flask import abort

def roles_required(*allowed_roles):
    """
    Decorator that checks if the current user has any of the specified roles.
    If the user is not authenticated or does not have one of the required roles,
    a 403 Forbidden error is raised.
    
    Usage:
    @app.route('/admin')
    @login_required
    @roles_required('Admin')
    def admin_dashboard():
        return 'Admin dashboard'
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role not in allowed_roles:
                abort(403)
            return fn(*args, **kwargs)
        return wrapper
    return decorator
