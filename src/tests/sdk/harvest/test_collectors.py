import src.sdk.harvest.collectors as collectors
from src.core.types import Any


def test_submodules_collector(mocker: Any):
    """Should copy for local file and not attempt download"""
    dummy_class = list(collectors.submodules())[0]
    data = list(dummy_class())
    
    expected = {
        "title": "A Fork in the Road",
        "synopsis": "Baby loves have fun",
        "imdb_code": "wtt00000000",
        "genres": ["Action", "Comedy", "Crime"],
        "creator_key": "0xee99ceff640d37edd9cac8c7cff4ed4cd609f435",
        "speech_language": "en",
        "release_year": 2010,
        "runtime": 105.0,
        "mpa_rating": "PG",
        "rating": 6.0,
    }

    assert data == [expected]
