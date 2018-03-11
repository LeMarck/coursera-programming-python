from functools import wraps
from json import dumps


def to_json(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return dumps(func(*args, **kwargs))

    return wrapper
