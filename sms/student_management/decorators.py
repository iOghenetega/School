from flask_jwt_extended import get_jwt, verify_jwt_in_request
from functools import wraps
from flask import jsonify
from http import HTTPStatus
from student_management.models import User


# this function was included here to avoid circular import
def get_user_type(pk: int):
    """ Get the type a user belong 
    param:
        pk : user id
    """
    user = User.query.filter_by(id=pk).first()
    if user:
        return user.user_type
    return None


def admin_required():
    """
    The following decorator provides endpoint security through the use of JSON Web Tokens.

    When applied to any route, the decorator will only permit access to the endpoint if the request includes a user type of admin.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            print(claims)
            if get_user_type(claims['sub']) == 'admin':
                return fn(*args, **kwargs)
            return jsonify({'msg': "Admin only!"}), HTTPStatus.UNAUTHORIZED
        return decorator
    return wrapper


def staff_required():
    """
    This code decorator applies protection to an endpoint by requiring JSON Web Tokens.
    The endpoint can only be accessed if the request contains a user type of either admin or teacher, as specified by the decorator.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if get_user_type(claims['sub']) == 'admin' or get_user_type(claims['sub']) == 'teacher':
                return fn(*args, **kwargs)
            return jsonify({'msg': "Staff Only!"}), HTTPStatus.UNAUTHORIZED
        return decorator
    return wrapper


def instructor_required():
    """
    This is a decorator designed to safeguard an endpoint using JSON Web Tokens.

    Once applied to a route, the endpoint will only be accessible if the request includes a user type of instructor, as specified by the decorator.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if get_user_type(claims['sub']) == 'teacher':
                return fn(*args, **kwargs)
            return jsonify({'msg': "Student Only!"}), HTTPStatus.UNAUTHORIZED
        return decorator
    return wrapper


def student_required():
    """
    This is a decorator that adds protection to an endpoint using JSON Web Tokens.

    When applied to a route, the endpoint can only be accessed if the request contains a user type of student, as specified by the decorator
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if get_user_type(claims['sub']) == 'student':
                return fn(*args, **kwargs)
            return jsonify({'msg': "Student Only!"}), HTTPStatus.UNAUTHORIZED
        return decorator
    return wrapper
