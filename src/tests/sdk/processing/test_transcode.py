import pytest
import src.core.exceptions as exceptions
import src.sdk.processing.transcode as transcode

from src.core.types import Any, Path
from src.sdk.processing.transcode.types import (
    Representations as REPR,
    Sizes,
    VideoInput,
    Size,
)


class MockFFProbe:
    ...


class MockMedia:
    def auto_generate_representations(self, *args: Any, **kwargs: Any):
        ...

    def __getattr__(self, name: str) -> Any:
        def method(*args: Any, **kwargs: Any):
            return self

        return method  # type: ignore


class MockInput(VideoInput):
    def __init__(self, input: Path, **options: Any):
        self._media = MockMedia()  # type: ignore
        self._probe = MockFFProbe()  # type: ignore
        self._path = input

    def get_media(self):
        return self._media

    def get_path(self):
        return self._path

    def get_size(self):
        return Size(100, 100)

    def get_duration(self):
        return 10.1


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
        representation = transcode.quality(size)
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
            transcode.quality(size)


def test_valid_input(mocker: Any):
    """Should instance a valid input"""
    mocker.patch(
        "src.sdk.processing.transcode.video.VideoInput",
        return_value=MockInput(Path("test")),
    )

    input_ = transcode.input(Path("test"))
    assert input_.get_size().width == 100
    assert input_.get_size().height == 100
    assert input_.get_path() == Path("test")
    assert input_.get_duration() == 10.1
