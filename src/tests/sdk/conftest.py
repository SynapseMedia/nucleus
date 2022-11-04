import pytest
from src.sdk.cache.models import Movie, Media
from src.sdk.cache import MediaType

example_path = "src/tests/core/fixture/watchit.png"


@pytest.fixture
def mock_movie():
    """Fixture to provide a mocking for movie"""
    resource = Media(
        route=example_path,
        type=MediaType.IMAGE,
    )

    return Movie(
        title="Test",
        imdb_code="wt00000000",
        creator_key="0x0",
        mpa_rating="PG",
        rating=5,
        runtime=90,
        release_year=1970,
        synopsis="",
        speech_language="en",
        publish_date=1666726838.7003856,
        genres=["Sci-fi", "Horror"],
        resources=[resource],
    )
