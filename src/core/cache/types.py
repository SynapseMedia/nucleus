from sqlite3 import Connection, Cursor, Row

# Query its a intuitive alias for query string
# Dont use a comment when you can use a right type to reveal the intent.
Query = str

__all__ = ["Connection", "Cursor", "Row", "Query"]
