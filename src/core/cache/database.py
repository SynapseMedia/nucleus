import sqlite3
import contextlib
import src.core.logger as logger

from src.core.types import Iterator, Any
from .constants import DB_DEFAULT
from .types import Connection


def connect(db_path: str = DB_DEFAULT, **kwargs: Any):
    """Db connection factory
    If path is not found, a new database file is created.

    :param db_path: sqlite file path
    :return: connection to database
    :rtype: Connection
    """
    # Explicit is better than implicit
    logger.log.info(f"Connecting to {db_path}")
    # ref: https://docs.python.org/3/library/sqlite3.html#how-to-write-adaptable-objects
    return sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES, **kwargs)


@contextlib.contextmanager
def connection(db_path: str = DB_DEFAULT, **kwargs: Any) -> Iterator[Connection]:
    """Context db connection

    :param db_path: sqlite file path
    :return: connection to database
    :rtype: Connection
    """
    # Explicit is better than implicit
    yield connect(db_path, **kwargs)


def is_open(conn: Connection) -> bool:
    """Check if connection is open.

    :param conn: connection to check
    :return: True if connection is open or False otherwise
    :rtype: bool
    """
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        return cursor is not None
    except Exception:
        return False


__all__ = ["connect", "connection", "is_open"]
