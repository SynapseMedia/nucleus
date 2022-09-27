# Convention for importing types
from src.core.types import Sequence, List
from .types import Connection, Cursor, Row, Query

# Exception for relative internal importing
from .decorator import connected


@connected
def _run(conn: Connection, q: Query, *args: Sequence[str]) -> Cursor:
    """Execute a custom query in database connection.

    :param conn: The out of the box connection to database
    :param q: The query to be executed
    :rtype: Cursor
    :returns: A Cursor to interface with
    """

    cursor = conn.cursor()
    return cursor.execute(q, *args)


@connected
def get(conn: Connection, q: Query, *args: Sequence[str]) -> Row:
    """Return one resolved entry

    :param q: The query to be returned
    :rtype: Row
    :return: Return an object matching the given query
    """

    res = _run(conn, q, *args)
    return res.fetchone()


@connected
def all(conn: Connection, q: Query, *args: Sequence[str]) -> List[Row]:
    """Return all resolved entries

    :param q: The query to be returned
    :rtype: List[Row]
    :return: Return a list of objects matching the given query
    """

    res = _run(conn, q, *args)
    return res.fetchall()


@connected
def exec(conn: Connection, q: Query, *args: Sequence[str]) -> bool:
    """Execute INSERT, UPDATE, DELETE, and REPLACE operations in the database.

    This method execute any write operations on the database.
    :param q: The query to be executed
    :rtype: bool
    :return: True if successful executed otherwise False
    """

    cursor = _run(conn, q, *args)
    # Read-only attribute that provides the number of modified rows for INSERT, UPDATE, DELETE, and REPLACE statements.
    # ref: https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor
    return cursor.rowcount > 0


def batch(conn: Connection, q: Query, *args: Sequence[str]) -> int:
    """Execute batch operations in the database.

    This method execute multiple any write operations on the database.
    :param q: The query to be executed
    :rtype: int
    :return: number of modified rows in the database
    """
    cursor = conn.cursor()
    cursor.executemany(q, *args)
    return cursor.rowcount


__all__ = [
    "get",
    "all",
    "exec",
    "batch",
]
