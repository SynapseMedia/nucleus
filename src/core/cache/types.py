from sqlite3 import Connection, Cursor, Row
from src.core.types import NamedTuple, Sequence, Any


# Query  type hold the needed data to commit a query to sqlite
# ref: https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor.execute
class Query(NamedTuple):
    sql: str  # placeholder query template
    values: Sequence[Any] = [] # bounded values for template


__all__ = ["Connection", "Cursor", "Row", "Query"]
