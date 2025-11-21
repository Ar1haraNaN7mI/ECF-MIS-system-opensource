from flask import jsonify, request
from functools import wraps

def success_response(data=None, message="Success", status_code=200):
    """Standard success response format"""
    response = {
        'success': True,
        'message': message,
        'data': data
    }
    return jsonify(response), status_code

def error_response(message="Error", status_code=400, errors=None):
    """Standard error response format"""
    response = {
        'success': False,
        'message': message,
        'errors': errors
    }
    return jsonify(response), status_code

def validate_json(f):
    """Decorator to validate JSON request"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return error_response("Request must be JSON", 400)
        return f(*args, **kwargs)
    return decorated_function

def handle_exceptions(f):
    """Decorator to handle exceptions"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            return error_response(str(e), 400)
        except Exception as e:
            return error_response(f"Internal server error: {str(e)}", 500)
    return decorated_function

