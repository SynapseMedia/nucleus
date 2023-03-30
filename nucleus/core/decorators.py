import functools
from nucleus.core.types import Any, Func, ExceptionType


def proxy_exception(*, expected: ExceptionType, target: ExceptionType) -> Func:
    """It decorate database operations to handle underlying exceptions and raise a new standard exception"""

    def decorator(func: Func):
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any):
            try:
                return func(*args, **kwargs)
            except expected as e:
                raise target(
                    f"raised exception during call to `{func.__name__}`: {str(e)}"
                )

        return wrapper

    return decorator
