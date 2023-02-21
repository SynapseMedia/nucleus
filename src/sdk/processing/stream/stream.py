from __future__ import annotations

from src.core.types import Any, Path, Dict, Sequence
from .types import Stream, Quality


class Streaming:
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

    def __getattr__(self, name: str) -> Streaming:
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

    def transcode(self, output_dir: Path, **kwargs: Any):
        """Start transcoding process
        :param output_dir: the dir to store resulting video
        :return: stream gear object
        :rtype: Stream
        """
        self._stream = Stream(
            output=output_dir,
            format=self._protocol,
            **kwargs,
            **self._params,
        )

        # run transcoding process
        self._stream.transcode_source()

    def terminate(self):
        self._stream.terminate()


def input(input_file: Path, **options: Any) -> Streaming:
    """Factory ffmpeg input interface from file

    :param input_file: Path to video
    :return: Input interface
    :rtype: Input
    """
    return Streaming(input_file, **options)  # type: ignore
