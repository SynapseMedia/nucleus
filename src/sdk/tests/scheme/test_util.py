from src.sdk.scheme import util


# Unit tests
def test_fit_image_resource_from_dag(mocker):
    """Should return valid image scheme fit for MediaScheme"""
    cid = "QMmmmTEST"
    image_dag = {
        "Links": [
            {"Name": "small.jpg"},
            {"Name": "medium.jpg"},
            {"Name": "large.jpg"},
        ]
    }

    expected_output = {
        "route": cid,
        "index": {
            "small": "/image/small.jpg",
            "medium": "/image/medium.jpg",
            "large": "/image/large.jpg",
        },
    }

    mocker.patch("src.sdk.scheme.util.dag_get", return_value=image_dag)
    assert util.fit_image_resource_from_dag(cid) == expected_output


# Unit tests
def test_fit_video_hls_resource_from_dag(mocker):
    """Should return valid video scheme fit for MediaScheme hls"""
    cid = "QMmmmTEST"
    hls_dag = {
        "Links": [
            {"Name": "hls"},
        ]
    }

    expected_output = {
        "route": cid,
        "index": {
            "hls": "/movie/hls/index.m3u8",
        },
    }

    mocker.patch("src.sdk.scheme.util.dag_get", return_value=hls_dag)
    assert util.fit_video_resource_from_dag(cid) == expected_output


# Unit tests
def test_fit_video_dash_resource_from_dag(mocker):
    """Should return valid video scheme fit for MediaScheme hls"""
    cid = "QMmmmTEST"
    dash_dag = {
        "Links": [
            {"Name": "dash"},
        ]
    }

    expected_output = {
        "route": cid,
        "index": {
            "dash": "/movie/dash/index.mpd",
        },
    }

    mocker.patch("src.sdk.scheme.util.dag_get", return_value=dash_dag)
    assert util.fit_video_resource_from_dag(cid) == expected_output
