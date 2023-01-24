import pytest
from src.sdk.harvest.models import Movie, Media
from src.sdk.harvest import MediaType



@pytest.fixture
def mock_movie():
    """Fixture to provide a mocking for movie"""
    resource = Media(
        route="src/tests/_mock/files/watchit.png",
        type=MediaType.IMAGE,
    )

    return Movie(
        title="A Fork in the Road",
        imdb_code="wtt00000000",
        creator_key="0xee99ceff640d37edd9cac8c7cff4ed4cd609f435",
        mpa_rating="PG",
        rating=6.0,
        runtime=105.0,
        release_year=2010,
        synopsis="Baby loves have fun",
        speech_language="en",
        publish_date=1669911990.9270618,
        genres=["Action", "Comedy", "Crime"],
        resources=[resource],
    )


@pytest.fixture
def mock_movie2():
    """Fixture to provide a mocking for movie"""
    resource = Media(
        route="src/tests/_mock/files/watchit.png",
        type=MediaType.IMAGE,
    )

    return Movie(
        title="Test 2",
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
