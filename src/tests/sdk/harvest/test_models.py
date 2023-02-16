import copy

from mock import patch
from src.core.types import Any
from src.sdk.harvest import Codex


def test_model_freeze(mock_models: Codex, setup_database: Any):
    """Should commit a valid mutation of movies"""
    with patch("src.core.cache.database.sqlite3") as mock:
        conn = setup_database
        mock.connect.return_value = conn  # type: ignore
        # eg. Movie(...).save()
        stored = mock_models.save()

        cursor = conn.cursor()
        query = cursor.execute("SELECT m FROM codex")
        rows = query.fetchone()

        assert rows[0] == mock_models
        assert stored


def test_movie_batch_freeze(mock_models: Codex, setup_database: Any):
    """Should commit a batch mutation of movies"""
    with patch("src.core.cache.database.sqlite3") as mock:
        conn = setup_database
        mock.connect.return_value = conn  # type: ignore
        model2 = copy.deepcopy(mock_models)
        model2.metadata.title = "The new boy"
            
        expected = [mock_models, model2]
        saved = mock_models.batch_save(iter(expected))
        result = mock_models.all()

        assert list(result) == expected
        assert all(saved)


def test_movie_fetch_frozen(mock_models: Codex, setup_database: Any):
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


def test_movie_get_frozen(mock_models: Codex, setup_database: Any):
    """Should query a valid get of a movie"""
    with patch("src.core.cache.database.sqlite3") as mock:
        conn = setup_database
        mock.connect.return_value = conn  # type: ignore

        # store a movie
        mock_models.save()
        result = Codex.get()
        movies = result
        assert movies == mock_models
