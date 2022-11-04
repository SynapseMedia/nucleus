import pytest
import sqlite3


@pytest.fixture
def setup_database():
    """Fixture to set up the in-memory database with test data"""
    conn = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
    conn.execute("CREATE TABLE IF NOT EXISTS movies(m movie);")
    yield conn
