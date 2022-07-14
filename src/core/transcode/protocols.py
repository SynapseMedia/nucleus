from ffmpeg_streaming import Representation, Formats  # type: ignore

from ._out import progress  # type: ignore
from . import Streaming, Input
from ..types import Directory


class HLS(Streaming):
    _input: Input

    def __init__(self, input: Input):
        self.input = input
        self._hls = input._media.hls(self.codec)  # type: ignore

    def set_representation(self, repr: Representation):
        self._hls.representations(repr)

    @property
    def codec(self):
        return Formats.h264()  # type: ignore

    def transcode(self, output_dir: Directory):
        self._hls.output(output_dir, monitor=progress)


class DASH(Streaming):
    _input: Input

    def __init__(self, input: Input):
        self.input = input
        self._dash = input._media.dash(self.codec)  # type: ignore

    def set_representation(self, repr: Representation):
        self._dash.representations(repr)

    @property
    def codec(self):
        return Formats.vp9()  # type: ignore

    def transcode(self, output_dir: Directory):
        self._dash.output(output_dir, monitor=progress)
