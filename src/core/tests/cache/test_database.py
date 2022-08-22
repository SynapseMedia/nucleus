from src.core.files import exists
from src.core.cache.database import connection, DEFAULT_DB


def test_valid_connection_for_valid_file():
    """Should instance a valid connection with valid input file db"""
    with connection(DEFAULT_DB) as conn:
        assert conn.cursor() is not None
        assert exists(DEFAULT_DB) == True
