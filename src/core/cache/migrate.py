import src.core.files as files

from .decorator import connected
from .database import Connection, TABLES_SCRIPT, INDEX_SCRIPT


@connected
def tables(conn: Connection):
    with files.read(TABLES_SCRIPT) as schema:
        conn.executescript(schema)


@connected
def indexes(conn: Connection):
    with files.read(INDEX_SCRIPT) as index:
        conn.executescript(index)


@connected
def verify(conn: Connection):
    ...
