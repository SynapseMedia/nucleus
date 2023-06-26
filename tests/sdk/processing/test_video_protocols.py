from nucleus.sdk.processing import H264, HEVC, HLS, VP9

hls_settings = {'hls_time': 10, 'hls_list_size': 0, 'hls_playlist_type': 'vod', 'tag:v': 'hvc1'}


def test_hls_hevc_protocol():
    """Should return expected HLS+HEVC presets as dict"""

    protocol = HLS(HEVC())
    expected_protocol = {
        **hls_settings,
        'g': 100,
        'crf': 0,
        'keyint_min': 100,
        'sc_threshold': 0,
        'c:a': 'aac',
        'c:v': 'libx265',
        'x265-params': 'lossless=1',
    }

    assert dict(protocol) == expected_protocol


def test_hls_vp9_protocol():
    """Should return expected HLS+VP9 presets as dict"""

    protocol = HLS(VP9())
    expected_protocol = {
        **hls_settings,
        'c:a': 'aac',
        'c:v': 'libvpx-vp9',
    }

    assert dict(protocol) == expected_protocol


def test_hls_h264_protocol():
    """Should return expected HLS+VP9 presets as dict"""

    protocol = HLS(H264())
    expected_protocol = {
        **hls_settings,
        'bf': 1,
        'g': 100,
        'crf': 0,
        'keyint_min': 100,
        'sc_threshold': 0,
        'c:a': 'aac',
        'c:v': 'libx264',
    }

    assert dict(protocol) == expected_protocol
