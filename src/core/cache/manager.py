# Convention for importing types
from src.core.types import List
from .types import Connection, Cursor, Row, Query

# Exception for relative internal importing
from .decorator import connected


def _run(conn: Connection, q: Query) -> Cursor:
    """Execute a custom query in database connection.

    :param conn: The out of the box connection to database
    :param q: The query to be executed
    :rtype: Cursor
    :returns: A Cursor to interface with
    """

    cursor = conn.cursor()
    return cursor.execute(q.sql, q.values)


@connected
def get(conn: Connection, q: Query) -> Row:
    """Return one resolved entry

    :param q: The query to be returned
    :rtype: Row
    :return: Return an object matching the given query
    """

    cursor = _run(conn, q)
    return cursor.fetchone()


@connected
def all(conn: Connection, q: Query) -> List[Row]:
    """Return all resolved entries

    :param q: The query to be returned
    :rtype: List[Row]
    :return: Return a list of objects matching the given query
    """

    cursor = _run(conn, q)
    return cursor.fetchall()


@connected
def exec(conn: Connection, q: Query) -> Cursor:
    """Execute INSERT, UPDATE, DELETE, and REPLACE operations in the database.

    This method execute any write operations on the database.
    :param q: The query to be executed
    :rtype: bool
    :return: True if successful executed otherwise False
    """

    return _run(conn, q)


@connected
def batch(conn: Connection, q: Query) -> Cursor:
    """Execute batch operations in the database.

    This method execute multiple any write operations on the database.
    :param q: The query to be executed
    :rtype: int
    :return: number of modified rows in the database
    """
    cursor = conn.cursor()
    return cursor.executemany(q.sql, q.values)


__all__ = [
    "get",
    "all",
    "exec",
    "batch",
]
