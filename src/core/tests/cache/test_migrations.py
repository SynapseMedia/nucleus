import sqlite3
from mock import patch
from src.core.cache.migrate import tables

def conn():
    yield sqlite3.connect("file::memory:?cache=shared", uri=True)


def test_migrate_tables():
    """Should run migration for expected tables"""
    with patch("src.core.cache.database.connection", return_value=conn) as _c:
        print(_c)
        tables()
