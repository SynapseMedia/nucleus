import os
import src.core.fs as fs
import src.core.cache.database as database

from mock import patch
from src.core.constants import ROOT_DIR
from src.core.types import Any, Path


TEST_DB = f"{ROOT_DIR}/test.db"


def test_is_open_ok_for_opened_connection():
    """Should return True for valid opened connection"""
    with database.connection(TEST_DB) as conn:
        assert database.is_open(conn) is True
        os.remove(TEST_DB)


def test_is_open_fail_for_closed_connection(mocker: Any):
    """Should return False for valid opened connection"""
    with patch("src.core.cache.database.sqlite3") as mock:
        mock.connect().cursor.return_value = None  # type: ignore
        with database.connection(TEST_DB) as conn:
            assert database.is_open(conn) is False


def test_valid_connection_for_valid_file():
    """Should instance a valid connection with valid input file db"""
    with database.connection(TEST_DB) as conn:
        assert conn.cursor() is not None
        assert fs.exists(Path(TEST_DB)) is True
        os.remove(TEST_DB)
