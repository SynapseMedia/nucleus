import pytest

from nucleus.sdk.exceptions import ModelValidationError
from nucleus.sdk.harvest import Model
from nucleus.tests._mock.models import Movie


class ExampleModel(Model):
    age: int


def test_initialization_raise_model_validation_error():
    with pytest.raises(ModelValidationError):
        ExampleModel(age=10)  # type: ignore missing name, description


def test_parse_obj_raise_model_validation_error():
    with pytest.raises(ModelValidationError):
        ExampleModel.parse_obj({'age': 10})  # missing name, description again


def test_parse_raw_raise_model_validation_error():
    with pytest.raises(ModelValidationError):
        # missing name, description again
        ExampleModel.parse_raw('{"age": 123}')


def test_model_freeze(mock_models: Movie):
    """Should commit a valid mutation of movies"""
    # eg. Movie(...).save()
    stored = mock_models.save()
    rows = mock_models.get()
    assert rows == mock_models
    assert stored


def test_movie_fetch_frozen(mock_models: Movie):
    """Should query a valid fetch of movies"""
    # store a movie
    expected = [mock_models]
    result = mock_models.all()
    movies = list(result)
    assert movies == expected


def test_movie_get_frozen(mock_models: Movie):
    """Should query a valid get of a movie"""
    # store a movie
    mock_models.save()
    result = Movie.get()
    movies = result
    assert movies == mock_models
