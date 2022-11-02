import src.core.logger as logger
import functools
import contextlib

# ref: https://docs.python.org/es/3/library/functools.html
from src.core.types import ParamSpec, TypeVar, Callable, Any, Optional
from .constants import DB_ISOLATION_LEVEL
from .database import connect
from .types import Connection


T = TypeVar("T")
P = ParamSpec("P")


class Atomic(contextlib.ContextDecorator):
    """A base class that enables a context manager to also be used as a decorator.

    ref: https://docs.python.org/3/library/contextlib.html
    """

    conn: Connection
    auto_close: bool = True

    def __init__(self, auto_close: bool = False):
        self.auto_close = auto_close

    def __enter__(self):
        # Set connection with isolation level to turn off auto commit
        # ref: https://docs.python.org/3.4/library/sqlite3.html#sqlite3.Connection.isolation_level
        logger.log.info("Starting query execution")
        self.conn = connect(isolation_level=DB_ISOLATION_LEVEL)
        return self.conn

    def __call__(self, f: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(f)
        def _wrapper(*args: Any, **kwargs: Any):
            with self._recreate_cm():  # type: ignore
                # Get extra settings passed to decorator
                self.auto_close = kwargs.pop("auto_close", self.auto_close)
                return f(self.conn, *args, **kwargs)

        return _wrapper

    def __exit__(self, *_: Any):

        try:
            # If context execution goes fine return results
            self.conn.commit()
            logger.log.info("Commit completed")
        except Exception as e:
            # In case of any issue we should rollback
            self.conn.rollback()
            logger.log.error(f"Error after try to execute transaction: {e}")
            # Raise an exception to "alert" about the issue.
            # Error should never pass silently.
            # When you raise without arguments, the interpreter looks for the last exception raised and handled.
            # It then acts the same as if you used raise with the most recent exception type, value and traceback.
            raise
        finally:
            if self.auto_close:
                # After everything is done we should commit transactions and close the connection.
                self.conn.close()


def connected(f: Optional[Callable[..., Any]] = None) -> Any:
    """Decorate a method call with database.

    :param f: A function to execute in wrapper
    :returns: Wrapper function
    :rtype: Callable[..., T]
    """

    if not callable(f):
        return Atomic()

    @functools.wraps(f)
    def _wrapper(*args: P.args, **kwargs: P.kwargs) -> Any:
        # Get connection a pass it to func call
        return f(connect(), *args, **kwargs)

    # Return wrapper function
    return _wrapper


def atomic(f: Optional[Callable[..., Any]] = None, **kwargs: Any) -> Any:
    """Decorate executions made to database.
    This method enhance the execution of queries/transactions to database adding extra atomic capabilities.

    :param f: This function should contain any query or transaction to db.
    :returns: decorated function/context for atomic transaction
    :rtype: Callable[..., T]
    :raises Exception: if database transaction fail
    """
    if callable(f):
        # If atomic is called as decorator
        return Atomic()(f)
    # If atomic is called as context manager
    return Atomic(**kwargs)


__all__ = ["connected", "atomic"]
