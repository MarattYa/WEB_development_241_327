from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user, login_required

def check_rights(required_roles):
    def decorator(func):
        @wraps(func)
        @login_required
        def wrapper(*args, **kwargs):
            if current_user.role and current_user.role.name in required_roles:
                return func(*args, **kwargs)
            else:
                flash("У вас недостаточно прав для доступа к данной странице.", "danger")
                return redirect(url_for('index'))
        return wrapper
    return decorator