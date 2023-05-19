import nucleus.sdk.harvest as harvest
from nucleus.core.types import JSON

mock_collectors_dir = 'nucleus/tests/_mock/collectors/'


def test_load_collector(mock_raw_collected: JSON):
    """Should collect expected metadata from dummy collector"""
    # we get the collector from original source files and get the first known
    dummy = list(harvest.load(mock_collectors_dir))[0]
    data = list(dummy)

    assert data == [mock_raw_collected]


def test_merge_collector(mock_raw_collected: JSON, mock_raw_collected2: JSON):
    """Should merge collected metadata from collectors"""
    loaded_collectors = harvest.load(mock_collectors_dir)
    data_merged = harvest.merge(loaded_collectors)
    assert list(data_merged) == [mock_raw_collected, mock_raw_collected2]


def test_map_collector(mock_raw_collected: JSON, mock_raw_collected2: JSON):
    """Should map collected metadata from collectors"""
    loaded_collectors = harvest.load(mock_collectors_dir)
    data_merged = harvest.map(loaded_collectors)
    got_values = data_merged.values()
    got_keys = data_merged.keys()

    assert list(got_values) == [[mock_raw_collected], [mock_raw_collected2]]
    assert list(got_keys) == ['Dummy', 'File']
