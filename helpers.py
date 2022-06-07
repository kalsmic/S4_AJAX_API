from functools import wraps

from flask import request, make_response, jsonify
from werkzeug.exceptions import abort


# This is a decorator function we have written to validate the request
# payload
def validate_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = request.get_json()
        if not len(data) or data.get('name', None) == None:
            abort(make_response(jsonify(message='Please provide an name property '), 400))
        return func(*args, **kwargs, )

    return wrapper

# Note: A decorator is a design pattern in Python that allows a user to add new functionality to an existing object
# without modifying its structure. Decorators are usually called before the definition of a function you want to
# decorate.
