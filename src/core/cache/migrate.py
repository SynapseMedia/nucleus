import src.core.files as files

from .decorator import connected
from .database import Connection, TABLES_SCRIPT, INDEX_SCRIPT


@connected
def tables(conn: Connection):
    with files.read(TABLES_SCRIPT) as schema:
        cursor = conn.cursor()
        cursor.executescript(schema)


@connected
def indexes(conn: Connection):
    with files.read(INDEX_SCRIPT) as schema:
        cursor = conn.cursor()
        cursor.executescript(schema)


@connected
def verify(conn: Connection):
    ...
