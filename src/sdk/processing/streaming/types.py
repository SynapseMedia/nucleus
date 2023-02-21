from __future__ import annotations

from enum import Enum
from dataclasses import dataclass
from vidgear.gears import StreamGear  # type: ignore

# Convention for importing types
from src.core.types import Sequence, Any, Path, Dict
from .types import Quality, Stream


Stream = StreamGear


class Size:
    def __init__(self, width: int, height: int):

        self.width = width
        self.height = height

    def __str__(self) -> str:
        return f"{self.width}x{self.height}"


class FPS(float, Enum):
    F30 = 30.0
    F60 = 60.0
    F120 = 120.0


class Quality:
    def __init__(self, size: Size, fps: FPS):
        self.size = size
        self.fps = fps

    def __call__(self):
        return {
            "-framerate": self.fps,
            "-resolution": str(self.size),
        }


@dataclass(frozen=True)
class Sizes:
    Q144 = Size(256, 144)
    Q240 = Size(426, 240)
    Q360 = Size(640, 360)
    Q480 = Size(854, 480)
    Q720 = Size(1280, 720)
    Q1080 = Size(1920, 1080)
    Q2k = Size(2560, 1440)
    Q4k = Size(3840, 2160)


class Input:
    """Adapter streaming class to handle preset protocols usage"""

    _stream: Stream
    _params: Dict[str, Any]
    _protocol: str

    __protocols__ = ("hls", "dash")

    def __init__(self, input: Path, **kwargs: Any):
        """Initialize Stream params.
        For additional params please check: https://abhitronix.github.io/vidgear/latest/gears/streamgear/ssm/usage/
        """
        self._params = {"-video_source": input, **kwargs}

    def set_quality(self, qualities: Sequence[Quality]):
        """Add expected quality resolution for transcoded output
        :param qualities: quality list to output
        :return: None
        """
        quality_collection = [quality() for quality in qualities]
        self._params = {**self._params, **{"-streams": quality_collection}}

    def __getattr__(self, name: str) -> Input:
        """Dynamically set protocol to use in transcoding process

        :param name: the expected protocol name
        :return: Streaming object
        :rtype: Streaming
        """
        if not name in self.__protocols__:
            raise AttributeError("expected to call hls or dash methods")
        self._protocol = name  # set called protocol
        self._params = {
            **self._params,
            **{"-vcodec": "libx265" if name == "hls" else "libvpx-vp9"},
        }

        return self

    def transcode(self, output_dir: Path, **kwargs: Any) -> Stream:
        """Start transcoding process
        :param output_dir: the dir to store resulting video
        :return: stream gear object
        :rtype: Stream
        """
        streamer = Stream(
            output=output_dir,
            format=self._protocol,
            **kwargs,
            **self._params,
        )
        
        streamer.transcode_source()
        streamer.terminate()
        return streamer
