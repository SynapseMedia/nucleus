import src.core.files as files

from .constants import DB_TABLES_SCRIPT, DB_INDEX_SCRIPT
from .decorator import connected
from .types import Connection


@connected
def tables(conn: Connection) -> Connection:
    """Attempt to migrate tables from script file

    :param conn: The out of the box connection to database
    :rtype: Connection
    :return: Connection object
    :raises sqlite3.OperationalError: if migration fails

    """
    with files.read(DB_TABLES_SCRIPT) as schema:
        conn.executescript(schema)
    return conn


@connected
def indexes(conn: Connection) -> Connection:
    """Attempt to migrate indexes from script file

    :param conn: The out of the box connection to database
    :rtype: Connection
    :return: Connection object
    :raises sqlite3.OperationalError: if migration fails
    """
    with files.read(DB_INDEX_SCRIPT) as index:
        conn.executescript(index)
    return conn


__all__ = ["tables", "indexes"]
