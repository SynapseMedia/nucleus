import sqlite3
import contextlib
import src.core.logger as logger

from sqlite3 import Connection
from src.core.types import Iterator
from src.core.constants import PROJECT_ROOT, DB_NAME


# Alias for ordering flags
ASC = 1
DESC = -1

# Default connection sqlite3 file dir
DEFAULT_DB = f"{PROJECT_ROOT}/{DB_NAME}"


@contextlib.contextmanager
def connection(db_path: str = DEFAULT_DB) -> Iterator[Connection]:
    """Db connection factory.
    If path is not found, a new database file is created.

    :param db_path: sqlite file path
    :return: connection to database
    :rtype: Connection
    """
    # Explicit is better than implicit
    connection = sqlite3.connect(db_path)
    logger.log.info(f"Connecting to {db_path}")
    yield connection
