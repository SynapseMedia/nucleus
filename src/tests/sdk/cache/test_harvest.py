from mock import patch
from src.core.types import Any
from src.sdk.cache.types import Movie
from src.sdk.cache.harvest import freeze


def test_freeze(mock_movie: Movie, setup_database: Any):

    """Should return True for valid opened connection"""
    with patch("src.core.cache.database.sqlite3") as mock:
        conn = setup_database
        mock.connect.return_value = conn  # type: ignore
        stored = freeze(mock_movie, auto_close=False)

        movie_dict = mock_movie.dict()
        expected_rows = tuple(movie_dict.values())
        expected_keys = ",".join(movie_dict.keys())

        cursor = conn.cursor()
        query = cursor.execute("SELECT %s FROM movies" % expected_keys)
        rows = query.fetchall()

        assert rows[0] == expected_rows
        assert stored == True
