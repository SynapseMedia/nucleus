from src.core.types import Any
from src.core.cache.migrate import Connection, tables  # , indexes


def get_sqlite_master(conn: Connection) -> Any:
    response = conn.execute("SELECT name FROM sqlite_master")
    return response.fetchall()


def test_migrate_tables():
    """Should run migration for defined tables in .sql script"""
    conn = tables()  # Run tables migration
    # check if tables exists after migration
    migration_result = get_sqlite_master(conn)
    expected_tables = set(
        (
            ("movies",),
            ("movies_resources",),
        )
    )

    matched_result = set(migration_result) & expected_tables
    assert matched_result == expected_tables


# def test_migrate_indexes():
#     """Should run migration for expected indexes"""
#     conn = indexes()  # Run indexes migration
#     # check if index exists after migration
#     migration_result = get_sqlite_master(conn)
#     assert ("idx_imdb_code",) in set(migration_result)
