from .decorator import connected
from .types import Connection, Cursor


@connected
def tables(conn: Connection) -> Cursor:
    """Attempt to migrate tables from script file

    :param conn: The out of the box connection to database
    :rtype: Connection
    :return: Connection object
    :raises sqlite3.OperationalError: if migration fails
    """
    return conn.execute("CREATE TABLE IF NOT EXISTS movies(m movie);")


__all__ = ["tables"]
