import src.core.logger as logger

# ref: https://docs.python.org/es/3/library/functools.html
from functools import wraps
from src.core.types import ParamSpec, TypeVar, Callable
from .database import connection

T = TypeVar("T")
P = ParamSpec("P")


def connected(f: Callable[..., T]) -> Callable[..., T]:
    """Decorate a method call with database.

    :param f: A function to execute in wrapper
    :returns: Wrapper function
    :rtype: Callable[..., T]
    """

    @wraps(f)
    def _wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        # Start connection with default database
        with connection() as conn:
            # Get connection a pass it to func call
            return f(conn, *args, **kwargs)

    # Return wrapper function
    return _wrapper


def atomic(f: Callable[..., T]) -> Callable[..., T]:
    """Decorate executions made to database.
    This method enhance the execution of queries/transactions to database adding extra atomic capabilities.

    :param f: This function should contain any query or transaction to db.
    :returns: Wrapper function
    :rtype: Callable[..., T]
    :raises sqlite3.OperationalError: if database transaction fail
    """

    @wraps(f)
    def _wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        # Start connection with default database
        with connection() as conn:
            try:
                # If context execution goes fine return results
                result = f(conn, *args, **kwargs)
            except Exception as e:
                # In case of any issue we should rollback
                conn.rollback()
                logger.log.error(f"Error after try to execute transaction: {e}")
                # Raise an exception to "alert" about the issue.
                # Error should never pass silently.
                # When you raise without arguments, the interpreter looks for the last exception raised and handled.
                # It then acts the same as if you used raise with the most recent exception type, value and traceback.
                raise
            finally:
                # After everything is done we should commit transactions and close the connection.
                conn.commit()
                conn.close()

            return result

    # Return wrapper function
    return _wrapper
