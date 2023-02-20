from src.sdk.processing.transcode.types import H264, VP9
from src.sdk.processing.transcode.protocols import HLS, DASH

from src.tests.sdk.processing.test_transcode import MockMedia


def test_hls_protocol():
    """Should return a valid codec for HLS"""

    hls = HLS(MockMedia()) # type: ignore
    assert isinstance(hls.codec, H264)


def test_dash_protocol():
    """Should return a valid codec for DASH"""

    dash = DASH(MockMedia()) # type: ignore
    assert isinstance(dash.codec, VP9)
