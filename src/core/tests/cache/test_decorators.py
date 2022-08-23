import pytest
from mock import patch
from src.core.cache.database import Connection, is_open
from src.core.cache.decorator import connected, atomic


def test_connected():
    """Should start connection for decorated function and pass connection as param"""

    @connected
    def to_decorate_with_connection(conn: Connection):
        # Should pass the current connection to db
        assert is_open(conn) == True

    to_decorate_with_connection()


def test_atomic():
    """Should run statements in transactional atomic mode"""

    @atomic
    def to_decorate_with_atomic(conn: Connection):
        # Should pass the current connection to db
        assert conn.execute("SELECT 1").fetchone() == (1,)

    to_decorate_with_atomic()


def test_atomic_rollback():
    """Should fail running statements and rollback"""
    with patch("src.core.cache.database.sqlite3") as mock:
        _roll = mock.connect().rollback()  # type: ignore
        with pytest.raises(Exception) :
            @atomic
            def to_decorate_with_atomic(conn: Connection):
                # Should pass the current connection to db
                raise Exception("failing")

            to_decorate_with_atomic()
            _roll.assert_called()  # type: ignore
