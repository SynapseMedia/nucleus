import os
import pytest
import nucleus.core.cache.database as database
import nucleus.core.cache.decorator as decorator

from mock import patch
from nucleus.core.cache.database import Connection
from nucleus.core.cache.constants import DB_DEFAULT


def test_connected():
    """Should start connection for decorated function and pass connection as param"""

    @decorator.connected
    def to_decorate_with_connection(conn: Connection):
        # Should pass the current connection to db
        assert database.is_open(conn) is True

    to_decorate_with_connection()
    os.remove(DB_DEFAULT)


def test_atomic():
    """Should run statements in transactional atomic mode"""
    with patch("nucleus.core.cache.database.sqlite3") as mock:
        mock.connect().execute().fetchone.return_value = (1,)  # type: ignore
        _commit = mock.connect().commit  # type: ignore

        @decorator.atomic
        def to_decorate_with_atomic(conn: Connection):
            # Should pass the current connection to db
            assert conn.execute("SELECT 1").fetchone() == (1,)

        to_decorate_with_atomic()
        _commit.assert_called()  # type: ignore


def test_atomic_rollback():
    """Should fail running statements and rollback"""
    with patch("nucleus.core.cache.database.sqlite3") as mock:
        _roll = mock.connect().rollback  # type: ignore

        with pytest.raises(Exception):

            @decorator.atomic
            def to_decorate_with_atomic(_):
                # Should pass the current connection to db
                raise Exception("fail")

            to_decorate_with_atomic()
            _roll.assert_called()  # type: ignore