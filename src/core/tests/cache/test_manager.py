# from mock import patch
import pytest
import sqlite3

from src.core.types import Any
from src.core.cache.manager import get, all, exec, batch

batch_query = """
    INSERT INTO movies (
        imdb_code, 
        title, 
        creator_key,
        mpa_rating, 
        rating, 
        runtime, 
        release_year, 
        synopsis, 
        speech_language, 
        trailer_code, 
        date_uploaded 
    ) VALUES (?,?,?,?,?,?,?,?,?,?,?)
"""

sample_data = [
    (
        "wt000000",
        "Test",
        "0x00000",
        "PG",
        10,
        180,
        2020,
        "Happy day",
        "en",
        "",
        0,
    ),
    (
        "wt000002",
        "Test2",
        "0x00000",
        "PG",
        10,
        180,
        2020,
        "Happy day",
        "en",
        "",
        0,
    ),
]


@pytest.fixture
def setup_database():
    """Fixture to set up the in-memory database with test data"""
    conn = sqlite3.connect(":memory:")
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            -- imdb code is adopted from IMB movies site to handle an alpha-numeric id
            imdb_code TEXT KEY DESC,
            title TEXT KEY DESC,
            -- creator key itself is a public key from blockchain network
            creator_key TEXT,
            mpa_rating TEXT,
            rating REAL,
            runtime REAL,
            release_year INTEGER,
            synopsis TEXT,
            speech_language TEXT,
            trailer_code TEXT,
            date_uploaded REAL
        );
        """
    )

    yield conn


@pytest.fixture
def setup_data(setup_database: Any):
    conn = setup_database
    conn.executemany(batch_query, sample_data)
    yield conn


def test_get(setup_data: Any):
    """Should return the first result based on query"""
    with setup_data as c:
        (imdb_code, title) = get("SELECT imdb_code, title FROM movies", conn=c)
        assert title == "Test"
        assert imdb_code == "wt000000"


def test_all(setup_data: Any):
    """Should return a list of results based on query"""
    with setup_data as c:
        results: Any = all("SELECT imdb_code, title FROM movies LIMIT 0,2", conn=c)
        assert results == [sample_data[0][0:2], sample_data[1][0:2]]


def test_exec(setup_data: Any):
    """Should execute queries and return number of affected rows"""
    with setup_data as c:
        count: Any = exec("DELETE FROM movies WHERE imdb_code='wt000002'", conn=c)
        assert count > 0


def test_exec_fail(setup_data: Any):
    """Should fails on execute invalid queries and return 0 affected rows"""
    with setup_data as c:
        count: Any = exec("DELETE FROM movies WHERE imdb_code='invalid'", conn=c)
        assert count == 0


def test_batch(setup_database: Any):
    """Should insert batch queries into database"""
    with setup_database as c:
        count: Any = batch(batch_query, sample_data, conn=c)
        assert count == 2
