import src.sdk.harvest as harvest

from src.sdk.harvest import Movie
from src.core.types import Any


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


class File(Movie):
    """Example purpose class to show mapped types usage"""

    ...


def test_load_collector():
    """Should collect expected metadata from dummy collector"""
    # we get the collector from original source files and get the first known
    dummy = list(harvest.load(mock_collectors_dir))[0]
    data = list(dummy)
    assert data == [expected]


def test_merge_collector():
    """Should merge collected metadata from collectors"""
    loaded_collectors = harvest.load(mock_collectors_dir)
    data_merged = harvest.merge(loaded_collectors)

    expected2 = expected.copy()
    expected2.update({"title": "A in the Road"})

    got = list(data_merged)
    assert got == [expected, expected2]


def test_map_collector():
    """Should map collected metadata from collectors"""
    loaded_collectors = harvest.load(mock_collectors_dir)
    data_merged = harvest.map(loaded_collectors)

    expected2 = expected.copy()
    expected2.update({"title": "A in the Road"})

    got_values = data_merged.values()
    got_keys = data_merged.keys()

    assert list(got_values) == [[expected], [expected2]]
    assert list(got_keys) == ["dummy", "file"]


def test_parse_collector_map():
    """Should parse mapped collected metadata"""
    loaded_collectors = harvest.load(mock_collectors_dir)
    data_merged = harvest.map(loaded_collectors)

    map_types = {
        "file": File,
        "dummy": Movie,
    }

    results: Any = []
    for k, value in data_merged.items():
        source_type = map_types[k]
        parsed = tuple(harvest.parse(source_type, value))
        results.append(parsed[0])

    assert isinstance(results[1], File)
    assert isinstance(results[0], Movie)



def test_parse_collector_merge():
    """Should parse merged collected metadata"""
    loaded_collectors = harvest.load(mock_collectors_dir)
    data_merged = harvest.merge(loaded_collectors)

    parsed = harvest.parse(Movie, data_merged)
    got = [isinstance(x, Movie) for x in parsed] # type: ignore

    assert all(got) == True
    assert len(got) == 2
