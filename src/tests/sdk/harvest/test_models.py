import pytest
import src.sdk.exceptions as exceptions

from mock import patch
from src.core.types import Any
from src.sdk.harvest import Collection, Meta


class ExampleModel(Meta):
    age: int


def test_initialization_raise_model_validation_error():
    with pytest.raises(exceptions.ModelValidationError):
        ExampleModel(age=10)  # type: ignore missing name, description


def test_parse_obj_raise_model_validation_error():
    with pytest.raises(exceptions.ModelValidationError):
        ExampleModel.parse_obj({"age": 10})  # missing name, description again


def test_parse_raw_raise_model_validation_error():
    with pytest.raises(exceptions.ModelValidationError):
        ExampleModel.parse_raw('{"age": 123}')  # missing name, description again


def test_model_freeze(mock_models: Collection, setup_database: Any):
    """Should commit a valid mutation of movies"""
    with patch("src.core.cache.database.sqlite3") as mock:
        conn = setup_database
        mock.connect.return_value = conn  # type: ignore
        # eg. Movie(...).save()
        stored = mock_models.save()

        cursor = conn.cursor()
        query = cursor.execute("SELECT m FROM collection")
        rows = query.fetchone()

        assert rows[0] == mock_models
        assert stored


def test_movie_fetch_frozen(mock_models: Collection, setup_database: Any):
    """Should query a valid fetch of movies"""
    with patch("src.core.cache.database.sqlite3") as mock:
        conn = setup_database
        mock.connect.return_value = conn  # type: ignore

        # store a movie
        expected = [mock_models]
        result = mock_models.all()
        movies = list(result)
        assert movies == expected


def test_movie_get_frozen(mock_models: Collection, setup_database: Any):
    """Should query a valid get of a movie"""
    with patch("src.core.cache.database.sqlite3") as mock:
        conn = setup_database
        mock.connect.return_value = conn  # type: ignore

        # store a movie
        mock_models.save()
        result = Collection.get()
        movies = result
        assert movies == mock_models
