import pytest 
from src.core.types import Any
from src.core.cache.types import Cursor, Query
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
        trailer_link, 
        publish_date 
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
def setup_data(setup_database: Any):
    conn = setup_database
    conn.executemany(batch_query, sample_data)
    yield conn


def test_get(setup_data: Any):
    """Should return the first result based on query"""
    with setup_data as c:
        query = Query("SELECT imdb_code, title FROM movies")
        (imdb_code, title) = get(query, conn=c)
        assert title == "Test"
        assert imdb_code == "wt000000"


def test_all(setup_data: Any):
    """Should return a list of results based on query"""
    with setup_data as c:
        query = Query("SELECT imdb_code, title FROM movies LIMIT 0,2")
        results: Any = all(query, conn=c)
        assert results == [sample_data[0][0:2], sample_data[1][0:2]]


def test_exec(setup_data: Any):
    """Should execute queries and return number of affected rows"""
    with setup_data as c:
        query = Query("DELETE FROM movies WHERE imdb_code='wt000002'")
        cursor: Cursor = exec(query, conn=c)
        assert cursor.rowcount > 0


def test_exec_fail(setup_data: Any):
    """Should fails on execute invalid queries and return 0 affected rows"""
    with setup_data as c:
        query = Query("DELETE FROM movies WHERE imdb_code='invalid'")
        cursor: Cursor = exec(query, conn=c)
        assert cursor.rowcount == 0


def test_batch(setup_database: Any):
    """Should insert batch queries into database"""
    with setup_database as c:
        query = Query(batch_query, sample_data)
        cursor: Cursor = batch(query, conn=c)
        assert cursor.rowcount == 2
