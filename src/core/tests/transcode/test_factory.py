import pytest
from typing import Any
from ffmpeg_streaming._format import H264, VP9  # type: ignore

from src.core.types import Directory
from src.core.exceptions import InvalidVideoQuality, InvalidStreamingProtocol
from src.core.transcode import REPR, Sizes, FormatID, Input, Size
from src.core.transcode.protocols import HLS, DASH
from src.core.transcode.factory import quality, streaming, input


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


def test_quality():
    """Should return a valid quality based on video size"""

    # Sizes hold each size as key and
    # each value as max quality supported
    sizes = {
        Sizes.Q480: REPR.R480p,
        Sizes.Q720: REPR.R720p,
        Sizes.Q1080: REPR.R1080p,
        Sizes.Q2k: REPR.R2k,
        Sizes.Q4k: REPR.R4k,
    }

    for size, high in sizes.items():
        representation = quality(size)
        # Expect always  the higher quality = size
        # expect always the lower quality = R360p
        higher = representation[-1]  # type: ignore
        lower = representation[0]  # type: ignore
        assert higher == high
        assert lower == REPR.R360p


def test_invalid_quality():
    """Should raise exception with invalid quality"""
    # All sized < 480 are not supported
    sizes = {
        Sizes.Q144,
        Sizes.Q240,
        Sizes.Q360,
    }

    for size in sizes:
        with pytest.raises(InvalidVideoQuality):
            quality(size)


def test_streaming_protocol():
    """Should return a valid streaming protocol for a valid protocol id"""

    with streaming(FormatID.Mp4, input=MockInput(Directory("test"))) as hls:
        assert isinstance(hls, HLS)
        assert isinstance(hls.codec, H264)
    with streaming(FormatID.Webm, input=MockInput(Directory("test"))) as dash:
        assert isinstance(dash, DASH)
        assert isinstance(dash.codec, VP9)


def test_invalid_streaming_protocol():
    """Should raise an exception for invalid protocol id"""

    with pytest.raises(InvalidStreamingProtocol):
        with streaming(0, input=MockInput("fail")):  # type: ignore
            pass


def test_valid_input(mocker: Any):
    """Should instance a valid input"""
    mocker.patch(
        "src.core.transcode.factory.Input", return_value=MockInput(Directory("test"))
    )
    with input(Directory("test")) as _input:
        assert _input.get_video_size().width == 100
        assert _input.get_video_size().height == 100
        assert _input.get_path() == Directory("test")
        assert _input.get_duration() == 10.1
