from sqlite3 import Connection, Cursor, Row
from src.core.types import NamedTuple, Sequence, Any


# Query  type hold the needed data to commit a query to sqlite
# ref: https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor.execute
class Query(NamedTuple):
    sql: str  # placeholder query template
    params: Sequence[Any] = []  # bounded params for template


class Condition(NamedTuple):
    fields: Sequence[Any]

    def __str__(self):
        sql = "WHERE %s"
        sql_fields = map(lambda x: f"{x} = ?", self.fields)
        return sql % " AND ".join(sql_fields)


__all__ = ["Connection", "Cursor", "Row", "Query"]
