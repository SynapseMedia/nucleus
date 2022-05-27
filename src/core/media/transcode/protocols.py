from . import Streaming, Input
from ._util import progress
from ffmpeg_streaming import Representation, Formats
from ...types import Directory


class HLS(Streaming):
    def __init__(self, input: Input):
        super().__init__(input)
        self._hls = input.media.hls(self.codec)

    def set_representation(self, repr: Representation):
        self._hls.representations(repr)

    @property
    def codec(self):
        return Formats.h264()

    def transcode(self, output_dir: Directory):
        self._hls.output(output_dir, monitor=progress)


class DASH(Streaming):
    def __init__(self, input: Input):
        super().__init__(input)
        self._dash = input.media.dash(self.codec)

    def set_representation(self, repr: Representation):
        self._dash.representations(repr)

    @property
    def codec(self):
        return Formats.vp9()

    def transcode(self, output_dir: Directory):
        self._dash.output(output_dir, monitor=progress)
