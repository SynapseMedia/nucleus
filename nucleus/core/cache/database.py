import contextlib
import sqlite3

from nucleus.core.exceptions import DatabaseError
from nucleus.core.types import Any, Iterator

from .constants import DB_DEFAULT
from .types import Connection


def connect(db_path: str = DB_DEFAULT, **kwargs: Any) -> Connection:
    """Db connection factory.
    If path is not found, a new database file is created.
    Connection is set to use Row as default row_factory.
    ref: https://docs.python.org/3/library/sqlite3.html

    :param db_path: Sqlite file path
    :return: Connection to database
    :param **kwargs: Any extra arguments to pass to sqlite connector
    :raises DatabaseError: If any error occurs during connection creation
    """

    try:
        # Connect and sets the row_factory to the callable sqlite3.Row, which
        # converts the plain tuple into a more useful object.
        return sqlite3.connect(
            db_path,
            detect_types=sqlite3.PARSE_DECLTYPES,
            **kwargs,
        )
    except sqlite3.Error as e:
        # proxy exception raising
        raise DatabaseError(f'error while trying to connect to database: {str(e)}')


@contextlib.contextmanager
def connection(db_path: str = DB_DEFAULT, **k: Any) -> Iterator[Connection]:
    """Context db connection

    :param db_path: Sqlite file path
    :return: Connection to database
    :raises DatabaseError: If any error occurs during connection creation
    """
    yield connect(db_path, **k)


def is_open(conn: Connection) -> bool:
    """Check if connection is open.

    :param conn: Connection to check
    :return: True if connection is open or False otherwise
    """
    cursor = conn.cursor()
    return cursor is not None


__all__ = ['connect', 'connection', 'is_open']
