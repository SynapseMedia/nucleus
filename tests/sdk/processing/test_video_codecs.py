from nucleus.sdk.processing import H264, HEVC, VP9


def test_vp9_codec_contains():
    """Should return true if contains expected codecs for vp9"""

    expected_codecs = [
        'libvpx',
        'libvpx-vp9',
        'aac',
        'libvo_aacenc',
        'libfaac',
        'libmp3lame',
        'libfdk_aac',
    ]

    vp9 = VP9()
    for codec in expected_codecs:
        assert codec in vp9


def test_hevc_codec_contains():
    """Should return true if contains expected codecs for HEVC"""

    expected_codecs = [
        'libx265',
        'h265',
        'aac',
        'libvo_aacenc',
        'libfaac',
        'libmp3lame',
        'libfdk_aac',
    ]

    hevc = HEVC()
    for codec in expected_codecs:
        assert codec in hevc


def test_h264_codec_contains():
    """Should return true if contains expected codecs for h264"""

    expected_codecs = [
        'libx264',
        'h264',
        'h264_afm',
        'h264_nvenc',
        'aac',
        'libvo_aacenc',
        'libfaac',
        'libmp3lame',
        'libfdk_aac',
    ]

    h264 = H264()
    for codec in expected_codecs:
        assert codec in h264
