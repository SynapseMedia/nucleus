import sqlite3
from mock import patch
from src.core.cache.migrate import tables, indexes


def conn():
    # Try to force use in memory database for tests
    yield sqlite3.connect("file::memory:?cache=shared", uri=True)


def test_migrate_tables():
    """Should run migration for defined tables in .sql script"""
    with patch("src.core.cache.database.connection", return_value=conn):
        conn_ = tables()  # Run tables migration
        # check if tables exists after migration
        response = conn_.execute("SELECT name FROM sqlite_master")
        table_list = response.fetchall()
        expected_tables = set(
            (
                ("movies",),
                ("movies_genres",),
                ("movies_movie_genre",),
                ("movies_resources",),
            )
        )
        
        matched_result = set(table_list) & expected_tables
        assert matched_result == expected_tables


def test_migrate_indexes():
    """Should run migration for expected tables"""
    with patch("src.core.cache.database.connection", return_value=conn):
        conn_ = indexes()  # Run indexes migration
        # check if index exists after migration
        response = conn_.execute("SELECT name FROM sqlite_master")
        table_list = response.fetchall()
        assert ("idx_imdb_code",) in set(table_list)
