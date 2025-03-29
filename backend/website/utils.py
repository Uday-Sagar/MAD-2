from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt
from functools import wraps

def role_required(required_role):
    def decorator(fn):
        @jwt_required()
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            if claims["role"] != required_role:
                return jsonify({'success': False, 'message': 'Unauthorized access'}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator


