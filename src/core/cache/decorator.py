import src.core.logger as logger

# ref: https://docs.python.org/3/library/contextlib.html
from contextlib import ContextDecorator

# ref: https://docs.python.org/es/3/library/functools.html
from functools import wraps
from src.core.types import ParamSpec, TypeVar, Callable, Any, Optional
from .constants import DB_ISOLATION_LEVEL
from .database import connect
from .types import Connection


T = TypeVar("T")
P = ParamSpec("P")


class Atomic(ContextDecorator):
    """A base class that enables a context manager to also be used as a decorator.

    ref: https://docs.python.org/3/library/contextlib.html
    """

    conn: Connection
    auto_close: bool

    def __enter__(self):
        # Set connection with isolation level to turn off auto commit
        # ref: https://docs.python.org/3.4/library/sqlite3.html#sqlite3.Connection.isolation_level
        logger.log.info("Starting query execution")
        self.conn = connect(isolation_level=DB_ISOLATION_LEVEL)
        self.auto_close = True  # close connection after execution?
        return self.conn

    def __call__(self, f: Callable[..., T]) -> Callable[..., T]:
        @wraps(f)
        def _wrapper(*args: Any, **kwargs: Any):
            with self._recreate_cm():  # type: ignore
                self.auto_close = kwargs.pop("auto_close", True)
                self.conn = kwargs.pop("conn", self.conn)
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
            # After everything is done we should commit transactions and close the connection.
            self.conn.close()
            pass


def connected(f: Callable[..., T]) -> Callable[..., T]:
    """Decorate a method call with database.

    :param f: A function to execute in wrapper
    :returns: Wrapper function
    :rtype: Callable[..., T]
    """

    @wraps(f)
    def _wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        # Get connection a pass it to func call
        return f(connect(), *args, **kwargs)

    # Return wrapper function
    return _wrapper


def atomic(f: Optional[Callable[..., Any]] = None) -> Any:
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
    return Atomic()


__all__ = ["connected", "atomic"]
