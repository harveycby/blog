from flask import abort
from flask_login import current_user
from functools import wraps

def role_required():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwrargs):
            if not current_user.is_authenticated:
                abort(404)
            return func(*args, **kwrargs)
        return wrapper
    return decorator