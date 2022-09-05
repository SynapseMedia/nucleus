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


"""
Example of usage:

1) using with context:

with atomic() as c:
    # override connection using `conn` kwarg 
    name = get("SELECT name from Movie WHERE id = (?)", 1, conn=c)
    exec("INSERT INTO Movie VALUES(?)", name, conn=c)

2) using atomic decorator:

@atomic
def transaction(c):
    name = get("SELECT name from Movie WHERE id = (?)", 1, conn=c)
    exec("INSERT INTO Movie VALUES(?)", name, conn=c)

3) using decorated simple pre-connected method:

@connected
def get(conn, query, params):
    ...

get("SELECT name from Movie WHERE id = (?)", 1)
    
"""


class Atomic(ContextDecorator):
    """A base class that enables a context manager to also be used as a decorator.

    ref: https://docs.python.org/3/library/contextlib.html
    """

    conn: Connection

    def __enter__(self):
        # Set connection with isolation level to turn off auto commit
        # ref: https://docs.python.org/3.4/library/sqlite3.html#sqlite3.Connection.isolation_level
        self.conn = connect(isolation_level=DB_ISOLATION_LEVEL)
        return self.conn

    def __call__(self, f: Callable[..., T]) -> Callable[..., T]:
        @wraps(f)
        def _wrapper(*args: Any, **kwargs: Any):
            with self._recreate_cm():  # type: ignore
                return f(self.conn, *args, **kwargs)

        return _wrapper

    def __exit__(self, *_: Any):

        try:
            # If context execution goes fine return results
            self.conn.commit()
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


def connected(f: Callable[..., T]) -> Callable[..., T]:
    """Decorate a method call with database.

    :param f: A function to execute in wrapper
    :returns: Wrapper function
    :rtype: Callable[..., T]
    """

    @wraps(f)
    def _wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        # override of connection if kwarg passed else start connection with default database
        conn = kwargs.pop("conn", connect())
        # Get connection a pass it to func call
        return f(conn, *args, **kwargs)

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
