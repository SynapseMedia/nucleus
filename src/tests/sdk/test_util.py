from src.sdk import util
from src.sdk.scheme.definition.movies import MovieScheme


def test_build_dir_without_group():
    """Should build output/input dir based on movie scheme imdb code and not by linked name"""
    mock_movie_scheme = MovieScheme().load({"imdb_code": "wtt0017075000"}, partial=True)
    extension = util.build_dir(mock_movie_scheme)
    expected = mock_movie_scheme.imdb_code

    assert extension == expected


def test_build_dir_with_group():
    """Should build output/input dir based on movie scheme imdb code with linked name"""
    mock_movie_scheme = MovieScheme().load(
        {"imdb_code": "wtt001707500", "group_name": "test"}, partial=True
    )
    extension = util.build_dir(mock_movie_scheme)
    expected = f"{mock_movie_scheme.group_name}/{mock_movie_scheme.imdb_code}"

    assert extension == expected
