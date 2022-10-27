from mock import patch
from src.core.types import Any
from src.sdk.cache.types import Movie
from src.sdk.cache.harvest import freeze


def test_freeze(mock_movie: Movie, setup_database: Any):
  
    """Should return True for valid opened connection"""
    with patch("src.core.cache.database.sqlite3") as mock:
        mock.connect.return_value = setup_database  # type: ignore
        freeze(mock_movie)
