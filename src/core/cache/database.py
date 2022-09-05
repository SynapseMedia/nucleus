import sqlite3
import contextlib
import src.core.logger as logger

from sqlite3 import Connection
from src.core.types import Iterator, Any
from src.core.constants import PROJECT_ROOT, DB_NAME, DB_ISOLATION


# Alias for ordering flags
ASC = 1
DESC = -1

# Default connection sqlite3 file dir
ISOLATION_LEVEL = DB_ISOLATION
DEFAULT_DB = f"{PROJECT_ROOT}/{DB_NAME}"
TABLES_SCRIPT = f"{PROJECT_ROOT}/src/core/cache/tables.sql"
INDEX_SCRIPT = f"{PROJECT_ROOT}/src/core/cache/indexes.sql"


def connect(db_path: str = DEFAULT_DB, **kwargs: Any):
    """Db connection factory
    If path is not found, a new database file is created.

    :param db_path: sqlite file path
    :return: connection to database
    :rtype: Connection
    """
    # Explicit is better than implicit
    connection = sqlite3.connect(db_path, **kwargs)
    logger.log.info(f"Connecting to {db_path}")
    return connection

@contextlib.contextmanager
def connection(db_path: str = DEFAULT_DB, **kwargs: Any) -> Iterator[Connection]:
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
