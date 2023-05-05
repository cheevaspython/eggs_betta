import logging
from functools import wraps
from typing import Any

from django.utils.datastructures import MultiValueDictKeyError


logger = logging.getLogger(__name__)

EXCEPTION_BOOK = {
    'KeyError': KeyError,
    'AttributeError': AttributeError,
    'TypeError': TypeError,
    'MultiValueDictKeyError': MultiValueDictKeyError,
    'IndexError': IndexError,
}

def try_decorator_param(exceptions: tuple, return_value: Any = None):
    def try_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if compare_entry_str_and_except_book(exceptions):
                errors = [EXCEPTION_BOOK[error] for error in exceptions]
                try:
                    return func(*args, **kwargs)
                except tuple(errors) as e:
                    logging.info('decorator', e, func.__name__)                                             
                    if return_value:
                        return return_value
            else:
                logging.warning('decorator.py wrong exception')
        return wrapper
    return try_decorator


def compare_entry_str_and_except_book(few_strs: tuple) -> bool:
    for string in few_strs:
        if string not in EXCEPTION_BOOK:
            return False
    return True
