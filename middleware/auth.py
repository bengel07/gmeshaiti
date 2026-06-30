from functools import wraps
from flask import session, redirect, jsonify

def login_requis(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            return jsonify({"error": "Not authenticated"}), 401
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("role") != "admin":
            return jsonify({"error": "Admin required"}), 403
        return f(*args, **kwargs)
    return decorated_function