from mock import patch
from src.core.types import Any, List
from src.sdk.cache.models import Movie


def test_movie_freeze(mock_movie: Movie, setup_database: Any):

    """Should return True for valid opened connection"""
    with patch("src.core.cache.database.sqlite3") as mock:
        conn = setup_database
        mock.connect.return_value = conn  # type: ignore
        stored = mock_movie.mutation.save()

        movie_dict = mock_movie.dict()
        expected_rows = tuple(movie_dict.values())
        expected_keys = ",".join(movie_dict.keys())

        cursor = conn.cursor()
        query = cursor.execute("SELECT %s FROM movies" % expected_keys)
        rows = query.fetchall()

        assert rows[0] == expected_rows
        assert stored == True


def test_movie_frozen(mock_movie: Movie, setup_database: Any):
    with patch("src.core.cache.database.sqlite3") as mock:
        conn = setup_database
        mock.connect.return_value = conn  # type: ignore

        # store a movie
        mock_movie.mutation.save()
        movies: List[Movie] = list(Movie.query.fetch())
        assert movies == [mock_movie]


# TODO test filter
# TODO test conditions
