import src.sdk.harvest as harvest

# Convention for importing types
from src.sdk.harvest import Movie

expected = {
    "title": "A Fork in the Road",
    "imdb_code": "wtt00000000",
    "creator_key": "0xee99ceff640d37edd9cac8c7cff4ed4cd609f435",
    "mpa_rating": "PG",
    "rating": 6.0,
    "runtime": 105.0,
    "synopsis": "Baby loves have fun",
    "release_year": 2010,
    "genres": ["Action", "Comedy", "Crime"],
    "speech_language": "en",
    "trailer_link": "",
    "publish_date": 1669911990.9270618,
    "resources": [],
}

mock_collectors_dir = "src/tests/_mock/collectors/"


def test_load_collector():
    """Should collect expected metadata from dummy collector"""
    # we get the collector from original source files and get the first known
    dummy = list(harvest.load(mock_collectors_dir))[0]
    data = list(dummy)
    assert data == [expected]


def test_parse_collector():
    """Should merge collected metadata from collectors"""
    loaded_collectors = harvest.load(mock_collectors_dir)
    data_merged = harvest.parse(loaded_collectors, Movie)

    expected2 = expected.copy()
    # Update the expected output for serialized model
    expected.update({"genres": "Action,Comedy,Crime"})
    expected2.update({"title": "A in the Road", "genres": "Action,Comedy,Crime"})
    got = list(map(lambda x: x.dict(), data_merged))

    assert got == [expected, expected2]
