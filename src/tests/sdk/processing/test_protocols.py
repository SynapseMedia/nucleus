import src.sdk.processing.transcode as transcode

from src.core.types import Path
from src.sdk.processing.transcode import Sizes
from src.sdk.processing.transcode.types import H264, VP9
from src.sdk.processing.transcode.protocols import HLS, DASH

from src.tests.sdk.processing.test_transcode import MockInput


def test_hls_protocol():
    """Should return a valid codec for HLS"""

    hls = HLS(MockInput(Path("test")))
    assert isinstance(hls.codec, H264)


def test_dash_protocol():
    """Should return a valid codec for DASH"""

    dash = DASH(MockInput(Path("test")))
    assert isinstance(dash.codec, VP9)


def test_input_mp4():
    path = Path("src/tests/_mock/files/video.mp4")
    out = Path("src/tests/_mock/files/video.dash")
    
    with transcode.input(path) as file:
        hls = HLS(file, hls_time=2)

        expected_quality = transcode.quality(Sizes.Q480)
        hls.set_representations(expected_quality)
        hls.transcode(out)
        
        
