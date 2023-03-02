from __future__ import annotations

# Convention for importing types
from src.core.types import Sequence, Any, Path, Mapping
from .types import Resolution, Stream


class Streaming:
    """Adapter streaming class to handle preset protocols usage"""

    _stream: Stream
    _params: Mapping[str, Any]
    _protocol: str = "hls"

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

    @classmethod
    def __stream__(cls, output_dir: Path) -> Stream:
        """Singleton stream gear factory

        :param output_dir: path to stream output
        :return: Stream object
        :rtype: Stream
        """
        if not cls._stream:
            cls._stream = Stream(
                output=output_dir,
                format=cls._protocol,
                **cls._params,
            )
        return cls._stream

    def resolutions(self, qualities: Sequence[Resolution]):
        """Add expected quality resolutions for transcoded output
        :param qualities: quality list to output
        :return: None
        """
        quality_collection = [quality.dict() for quality in qualities]
        self._params = {**self._params, **{"-streams": quality_collection}}

    def hls(self) -> Streaming:
        """set hls protocol to use in transcoding process

        :param name: the expected protocol name
        :return: Streaming object
        :rtype: Streaming
        """
        # set called protocol
        self._protocol = "hls"
        return self

    def dash(self) -> Streaming:
        """set dash protocol to use in transcoding process

        :param name: the expected protocol name
        :return: Streaming object
        :rtype: Streaming
        """
        # set called protocol
        self._protocol = "dash"
        return self

    def transcode(self, output_dir: Path):
        """Start transcoding process

        :param output_dir: path to stream output
        :return: stream gear object
        :rtype: Stream
        """

        # run transcoding process
        self.__stream__(output_dir).transcode_source()

    def terminate(self) -> None:
        """Finish transcode process"""
        if not self._stream:
            return

        self._stream.terminate()
