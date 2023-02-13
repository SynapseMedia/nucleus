import pytest
import src.core.exceptions as exceptions
import src.sdk.processing as media

from src.core.types import Directory, Any
from src.sdk.processing.transcode.types import (
    Representations as REPR,
    Sizes,
    Input,
    Size,
)


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
        representation = media.ffmpeg.quality(size)
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
        with pytest.raises(exceptions.InvalidVideoQuality):
            media.ffmpeg.quality(size)


def test_valid_input(mocker: Any):
    """Should instance a valid input"""
    mocker.patch(
        "src.core.transcode.ffmpeg.VideoInput",
        return_value=MockInput(Directory("test")),
    )
    with media.ffmpeg.input(Directory("test")) as _input:
        assert _input.get_video_size().width == 100
        assert _input.get_video_size().height == 100
        assert _input.get_path() == Directory("test")
        assert _input.get_duration() == 10.1
