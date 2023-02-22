from __future__ import annotations

# Convention for importing types
from src.core.types import Sequence, Any, Path, Dict
from .types import Resolution, Stream


class Streaming:
    """Adapter streaming class to handle preset protocols usage"""

    _stream: Stream
    _params: Dict[str, Any]
    _protocol: str

    __protocols__ = ("hls", "dash")

    def __init__(self, input: Path, **kwargs: Any):
        """Initialize Stream params.
        For additional params please check `stream_params` in:
        ref: https://abhitronix.github.io/vidgear/latest/gears/streamgear/ssm/usage/
        ref: https://ffmpeg.org/ffmpeg-all.html
        """

        # default params
        self._params = {
            "-video_source": input,
            **kwargs,
        }

    def set_resolutions(self, qualities: Sequence[Resolution]):
        """Add expected quality resolutions for transcoded output
        :param qualities: quality list to output
        :return: None
        """
        quality_collection = [quality.dict() for quality in qualities]
        self._params = {**self._params, **{"-streams": quality_collection}}

    def __getattr__(self, name: str) -> Streaming:
        """Dynamically set protocol to use in transcoding process

        :param name: the expected protocol name
        :return: Streaming object
        :rtype: Streaming
        """
        if name not in self.__protocols__:
            raise AttributeError("expected to call hls or dash methods")
        # set called protocol
        self._protocol = name
        return self

    def stream(self, output_dir: Path) -> Streaming:
        """Stream factory.

        :param output_dir: path to stream output
        :param kwargs: any additional arguments
        :return: Stream object
        :rtype: Stream

        """
        self._stream = Stream(
            output=output_dir,
            format=self._protocol,
            **self._params,
        )

        return self

    def transcode(self) -> Stream:
        """Start transcoding process

        :param output_dir: the dir to store resulting video
        :return: stream gear object
        :rtype: Stream
        :raises RuntimeError: if stream is not set before call 
        """

        if not self._stream:
            raise RuntimeError("expected stream to transcode")

        # run transcoding process
        self._stream.transcode_source()
        self._stream.terminate()
        return self._stream
