import src.sdk.harvest.collectors as collectors

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


def test_submodules_collector():
    """Should collect expected metadata from dummy collector"""
    dummy = list(collectors.load())[0]
    data = list(dummy)
    assert data == [expected]


def test_merge_collector():
    """Should merge collected metadata from collectors"""
    loaded_collectors = collectors.load()
    data_merged = collectors.merge(loaded_collectors)
    
    expected2 = expected.copy()
    expected2.update({"title": "A in the Road"})
    assert list(data_merged) == [expected, expected2]
