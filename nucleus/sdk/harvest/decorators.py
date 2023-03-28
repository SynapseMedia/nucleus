import sqlite3
import functools
import nucleus.sdk.exceptions as exceptions

from nucleus.core.types import Callable, Any


def with_standard_errors(func: Callable[..., Any]) -> Callable[..., Any]:
    """It decorate database operations to handle underlying exceptions and raise a new standard exception"""

    @functools.wraps(func)
    def wrapper(ref_: Any, *args: Any, **kwargs: Any):
        try:
            return func(ref_, *args, **kwargs)
        except sqlite3.ProgrammingError as e:
            raise exceptions.ModelManagerError(
                f"raised exception during `{func.__name__}`: {str(e)}"
            )

    return wrapper
