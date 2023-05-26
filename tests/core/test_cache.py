import os
from unittest.mock import patch

import nucleus.core.cache as cache
from nucleus.core.constants import ROOT_DIR
from nucleus.core.types import Path

TEST_DB = f'{ROOT_DIR}/test.db'


def test_is_open_ok_for_opened_connection():
    """Should return True for valid opened connection"""
    with cache.connection(TEST_DB) as conn:
        assert cache.is_open(conn) is True
        os.remove(TEST_DB)


def test_is_open_fail_for_closed_connection():
    """Should return False for valid opened connection"""
    with patch('nucleus.core.cache.database.sqlite3') as mock:
        mock.connect().cursor.return_value = None  # type: ignore
        with cache.connection(TEST_DB) as conn:
            assert cache.is_open(conn) is False


def test_valid_connection_for_valid_file():
    """Should instance a valid connection with valid input file db"""
    with cache.connection(TEST_DB) as conn:
        assert conn.cursor() is not None
        assert Path(TEST_DB).exists() is True
        os.remove(TEST_DB)
