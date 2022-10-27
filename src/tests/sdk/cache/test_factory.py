from src.sdk.cache.types import Movie
from src.sdk.cache.factory import query
from src.sdk.cache.constants import INSERT_MOVIE


def test_query(mock_movie: Movie):
    result = query(mock_movie, INSERT_MOVIE, exclude={"resources"})
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
