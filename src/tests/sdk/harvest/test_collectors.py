import copy
import src.sdk.harvest as harvest

from src.sdk.harvest.models import Model

mock_collectors_dir = "src/tests/_mock/collectors/"


def test_load_collector(mock_models: Model):
    """Should collect expected metadata from dummy collector"""
    # we get the collector from original source files and get the first known
    dummy = list(harvest.load(mock_collectors_dir))[0]
    data = list(dummy)
    assert data == [mock_models]


def test_merge_collector(mock_models: Model):
    """Should merge collected metadata from collectors"""
    loaded_collectors = harvest.load(mock_collectors_dir)
    data_merged = harvest.merge(loaded_collectors)

    expected2 = copy.deepcopy(mock_models)
    expected2.metadata.title = "A in the Road"

    got = list(data_merged)
    assert got == [mock_models, expected2]


def test_map_collector(mock_models: Model):
    """Should map collected metadata from collectors"""
    loaded_collectors = harvest.load(mock_collectors_dir)
    data_merged = harvest.map(loaded_collectors)

    expected2 = copy.deepcopy(mock_models)
    expected2.metadata.title = "A in the Road"

    got_values = data_merged.values()
    got_keys = data_merged.keys()

    assert list(got_values) == [[mock_models], [expected2]]
    assert list(got_keys) == ["dummy", "file"]


def test_parse_collector_merge():
    """Should parse merged collected metadata"""
    loaded_collectors = harvest.load(mock_collectors_dir)
    data_merged = harvest.merge(loaded_collectors)
    got = [isinstance(x, Model) for x in data_merged]  # type: ignore

    assert all(got)
    assert len(got) == 2
