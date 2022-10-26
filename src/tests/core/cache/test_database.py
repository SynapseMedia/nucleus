from mock import patch
from src.core.types import Any
from src.core.files import exists
from src.core.cache.database import connection, DB_DEFAULT, is_open


def test_is_open_ok_for_opened_connection():
    """Should return True for valid opened connection"""
    with connection(DB_DEFAULT) as conn:
        assert is_open(conn) is True


def test_is_open_fail_for_closed_connection(mocker: Any):
    """Should return False for valid opened connection"""
    with patch("src.core.cache.database.sqlite3") as mock:
        mock.connect().cursor.return_value = None  # type: ignore
        with connection(DB_DEFAULT) as conn:
            assert is_open(conn) is False


def test_valid_connection_for_valid_file():
    """Should instance a valid connection with valid input file db"""
    with connection(DB_DEFAULT) as conn:
        assert conn.cursor() is not None
        assert exists(DB_DEFAULT) is True
