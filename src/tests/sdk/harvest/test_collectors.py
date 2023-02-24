import src.sdk.harvest as harvest

from src.sdk.harvest import Collection

mock_collectors_dir = "src/tests/_mock/collectors/"


def test_load_collector(mock_models: Collection):
    """Should collect expected metadata from dummy collector"""
    # we get the collector from original source files and get the first known
    dummy = list(harvest.load(mock_collectors_dir))[0]
    data = list(dummy)
    assert data == [mock_models]


def test_merge_collector(mock_models: Collection, mock_models_B: Collection):
    """Should merge collected metadata from collectors"""
    loaded_collectors = harvest.load(mock_collectors_dir)
    data_merged = harvest.merge(loaded_collectors)
    assert list(data_merged) == [mock_models, mock_models_B]


def test_map_collector(mock_models: Collection, mock_models_B: Collection):
    """Should map collected metadata from collectors"""
    loaded_collectors = harvest.load(mock_collectors_dir)
    data_merged = harvest.map(loaded_collectors)

    got_values = data_merged.values()
    got_keys = data_merged.keys()

    assert list(got_values) == [[mock_models], [mock_models_B]]
    assert list(got_keys) == ["dummy", "file"]


def test_parse_collector_merge():
    """Should parse merged collected metadata"""
    loaded_collectors = harvest.load(mock_collectors_dir)
    data_merged = harvest.merge(loaded_collectors)
    got = [isinstance(x, Collection) for x in data_merged]  # type: ignore

    assert all(got)
    assert len(got) == 2
