from src.core.types import Directory
from src.sdk.processing.transcode.types import H264, VP9
from src.sdk.processing.transcode.protocols import HLS, DASH

from src.tests.sdk.processing.test_transcode import MockInput


def test_hls_protocol():
    """Should return a valid codec for HLS"""

    hls = HLS(MockInput(Directory("test")))
    assert isinstance(hls.codec, H264)


def test_dash_protocol():
    """Should return a valid codec for DASH"""

    dash = DASH(MockInput(Directory("test")))
    assert isinstance(dash.codec, VP9)
