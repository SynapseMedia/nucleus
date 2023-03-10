import pytest


@pytest.fixture
def mock_hls_presets():
    return {
        "c:v":  "libx265",
        "preset": "slow",
        "c:a": "aac",
        "sc_threshold": 0,
        "f": "hls",
        "crf": 0,
        "g": 100,
        "keyint_min": 100,
        "b:v": "128k",
        "x265-params": "lossless=1",
        "hls_time": 10,
        "hls_list_size": 0,
        "hls_playlist_type": "vod",
        "tag:v": "hvc1",
    }
