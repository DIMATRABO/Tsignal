from functools import wraps
from flask import request

def paginate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        page_number = request.args.get('page', default=1, type=int)
        page_size = request.args.get('page_size', default=10, type=int)
        kwargs['page_number'] = page_number
        kwargs['page_size'] = page_size
        return func(*args, **kwargs)
    return wrapper