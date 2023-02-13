from src.core.types import Directory, Any
from src.sdk.processing.transcode.types import Input, Size, H264, VP9
from src.sdk.processing.transcode.protocols import HLS, DASH


class MockMedia:
    def __getattr__(self, name: str) -> Any:
        return lambda _: name  # type: ignore


class MockInput(Input):
    def __init__(self, input: Directory, **options: Any):
        self._media = MockMedia()  # type: ignore
        self._path = input

    def get_path(self) -> Directory:
        return self._path

    def get_video_size(self) -> Size:
        return Size(100, 100)

    def get_duration(self) -> float:
        return 10.1


class MockFFProbe:
    pass


def test_hls_protocol():
    """Should return a valid codec for HLS"""

    hls = HLS(MockInput(Directory("test")))
    assert isinstance(hls.codec, H264)


def test_dash_protocol():
    """Should return a valid codec for DASH"""

    dash = DASH(MockInput(Directory("test")))
    assert isinstance(dash.codec, VP9)
