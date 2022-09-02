from sqlite3 import Cursor, Row
from src.core.types import Sequence, List

from .decorator import connected
from .database import Connection
from .types import Query


@connected
def exec(conn: Connection, q: Query, *args: Sequence[str]) -> Cursor:
    """Execute a query in database connection

    :param conn: The out of the box connection to database
    :param q: The query to be executed
    :rtype: Cursor
    :returns: A Cursor to interface with
    """

    cursor = conn.cursor()
    return cursor.execute(q, *args)


@connected
def get(conn: Connection, q: Query, *args: Sequence[str]) -> Row:
    """Return resolved entry

    :param q: The query to be returned
    :rtype: Any
    :return: Return an object matching the given query
    """

    res = exec(conn, q, *args)
    return res.fetchone()


@connected
def fetch(conn: Connection, q: Query, *args: Sequence[str]) -> List[Row]:
    """Return all resolved entries

    :param q: The query to be returned
    :return: Return a list of objects matching the given query
    """

    res = exec(conn, q, *args)
    return res.fetchall()


@connected
def upsert(conn: Connection, q: Query, *args: Sequence[str]) -> bool:
    """Create or update an entry in the database.

    Since the execution of the queries for CREATE and UPDATE are essentially similar in relation to the execution of sqlite3,
    a single method is established to execute these queries. Only the query define the real operation to exec.
    IMPORTANT: This is not an upsert operation underneath.

    eg.
        upsert("INSERT INTO table VALUES(?,?,?)", "a", "a", "a")
        upsert("UPDATE table SET a = ? WHERE a = ?", "a", "b")


    :param q: The query to be executed
    :rtype: bool
    :return: True if successful created entry otherwise False
    """

    cursor = exec(conn, q, *args)
    # Read-only attribute that provides the row id of the last inserted row.
    # It is only updated after successful INSERT or REPLACE statements using the execute() method.
    # The initial value of lastrowid is None.
    # ref: https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor
    return cursor.lastrowid is not None
