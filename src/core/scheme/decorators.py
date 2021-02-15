from functools import wraps
import src.core.scheme.validator as v


def check_valid_scheme(func):
    @wraps(func)
    def wrapper(self, **kwargs):
        context = func(self, **kwargs)
        return v.check(context)

    return wrapper
