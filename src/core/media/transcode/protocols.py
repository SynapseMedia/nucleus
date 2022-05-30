from . import Streaming, Input
from ._util import progress  # type: ignore
from ffmpeg_streaming import Representation, Formats, Format  # type: ignore
from ...types import Directory


class HLS(Streaming):
    input: Input

    def __init__(self, input: Input):
        self.input = input
        self._hls = input.media.hls(self.codec)  # type: ignore

    def set_representation(self, repr: Representation):
        self._hls.representations(repr)

    @property
    def codec(self):
        return Formats.h264()  # type: ignore

    def transcode(self, output_dir: Directory):
        self._hls.output(output_dir, monitor=progress)


class DASH(Streaming):
    input: Input

    def __init__(self, input: Input):
        self.input = input
        self._dash = input.media.dash(self.codec)  # type: ignore

    def set_representation(self, repr: Representation):
        self._dash.representations(repr)

    @property
    def codec(self):
        return Formats.vp9()  # type: ignore

    def transcode(self, output_dir: Directory):
        self._dash.output(output_dir, monitor=progress)
