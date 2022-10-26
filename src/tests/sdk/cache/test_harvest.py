
from src.core.types import Any
from src.sdk.cache.types import Movie
from src.sdk.cache.harvest import _query_from_movie, freeze  # type: ignore

mock_movie = Movie(
    title="Test",
    imdb_code="wt00000000",
    creator_key="0x0",
    mpa_rating="PG",
    rating=5,
    runtime=90,
    release_year=1970,
    synopsis="",
    speech_language="en",
    publish_date=1666726838.7003856,
    genres=["Sci-fi", "Horror"],
)

def test_query_from_movies():
    result = _query_from_movie(mock_movie)
    expected_sql = """INSERT INTO movies(title,imdb_code,creator_key,mpa_rating,rating,runtime,synopsis,release_year,genres,speech_language,publish_date,trailer_link) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)"""
    expected_values = [
        "Test",
        "wt00000000",
        "0x0",
        "PG",
        5.0,
        90.0,
        "",
        1970,
        "Sci-fi, Horror",
        "en",
        1666726838.7003856,
        None,
    ]

    assert result.values == expected_values
    assert result.sql == expected_sql


def test_freeze(setup_database: Any):
    """Should return True for valid opened connection"""
    conn = setup_database
    with conn as c:
        freeze(mock_movie, conn=c, auto_close=False)
