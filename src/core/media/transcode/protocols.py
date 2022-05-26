from . import Streaming, Input
from .util import progress
from ffmpeg_streaming import Representation, Formats


class HLS(Streaming):
    def __init__(self, input: Input):
        self._hls = input.media.hls(self.codec)
        super().__init__(input)

    def set_representation(self, repr: Representation):
        self._hls.representations(repr)

    @property
    def codec(self):
        return Formats.h264()

    def transcode(self, output_dir: str):
        self._hls.output(output_dir, monitor=progress)


class DASH(Streaming):
    def __init__(self, input: Input):
        self._dash = input.media.dash(self.codec)
        super().__init__(input)

    def set_representation(self, repr: Representation):
        self._dash.representations(repr)

    @property
    def codec(self):
        return Formats.vp9()

    def transcode(self, output_dir: str):
        self._dash.output(output_dir, monitor=progress)
