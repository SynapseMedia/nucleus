from mock import patch
from src.core.types import Any
from src.sdk.harvest import Model


def test_model_freeze(mock_models: Model, setup_database: Any):
    """Should commit a valid mutation of movies"""
    with patch("src.core.cache.database.sqlite3") as mock:
        conn = setup_database
        mock.connect.return_value = conn  # type: ignore
        # eg. Movie(...).save()
        stored = mock_models.save()

        cursor = conn.cursor()
        query = cursor.execute("SELECT m FROM models")
        rows = query.fetchone()

        assert rows[0] == mock_models
        assert stored


def test_movie_fetch_frozen(mock_models: Model, setup_database: Any):
    """Should query a valid fetch of movies"""
    with patch("src.core.cache.database.sqlite3") as mock:
        conn = setup_database
        mock.connect.return_value = conn  # type: ignore

        # store a movie
        mock_models.save()
        expected = [mock_models]
        result = mock_models.all()
        movies = list(result)
        assert movies == expected


def test_movie_get_frozen(mock_models: Model, setup_database: Any):
    """Should query a valid get of a movie"""
    with patch("src.core.cache.database.sqlite3") as mock:
        conn = setup_database
        mock.connect.return_value = conn  # type: ignore

        # store a movie
        mock_models.save()
        result = Model.get()
        movies = result
        assert movies == mock_models
