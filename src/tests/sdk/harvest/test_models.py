from mock import patch
from src.core.types import Any, List
from src.sdk.harvest import Movie

# TODO test filter
# TODO test bulk save
def test_movie_freeze(mock_movie: Movie, setup_database: Any):
    """Should commit a valid mutation of movies"""
    with patch("src.core.cache.database.sqlite3") as mock:
        conn = setup_database
        mock.connect.return_value = conn  # type: ignore
        # eg. Movie(...).save()
        stored = mock_movie.save()

        cursor = conn.cursor()
        query = cursor.execute("SELECT m FROM movies")
        rows = query.fetchone()

        assert rows[0] == mock_movie
        assert stored == True


def test_movie_fetch_frozen(mock_movie: Movie, setup_database: Any):
    """Should query a valid fetch of movies"""
    with patch("src.core.cache.database.sqlite3") as mock:
        conn = setup_database
        mock.connect.return_value = conn  # type: ignore

        # store a movie
        mock_movie.save()
        expected = [mock_movie]
        result = Movie.all()
        movies: List[Movie] = list(result)
        assert movies == expected


def test_movie_get_frozen(mock_movie: Movie, setup_database: Any):
    """Should query a valid get of a movie"""
    with patch("src.core.cache.database.sqlite3") as mock:
        conn = setup_database
        mock.connect.return_value = conn  # type: ignore

        # store a movie
        mock_movie.save()
        result = Movie.get()
        movies: Movie = result
        assert movies == mock_movie


