from nucleus.sdk.processing import BR, FPS, Custom, FrameSize


def test_frame_size_option():
    """Should return expected Size as dict"""

    size = FrameSize(100, 100)
    expected_size = {'s': '100x100'}
    assert dict(size) == expected_size


def test_fps_option():
    """Should return expected FPS as dict"""

    fps = FPS(60)
    expected_fps = {'r': 60}
    assert dict(fps) == expected_fps


def test_bitrate_overall_option():
    """Should return expected overall BR as dict"""

    bitrate = BR(120)
    expected_bitrate = {'b': '120k'}
    assert dict(bitrate) == expected_bitrate


def test_bitrate_option():
    """Should return expected video,audio BR as dict"""

    bitrate = BR(120, 60)
    expected_bitrate = {'b:v': '120k', 'b:a': '60k'}
    assert dict(bitrate) == expected_bitrate


def test_custom_option():
    """Should return expected custom option as dict"""

    custom = Custom(t=20, r=60)
    expected_custom = {'t': 20, 'r': 60}
    assert dict(custom) == expected_custom
