from . import Codec, Input
from .util import progress
from ffmpeg_streaming import Representation, Formats


class HLS(Codec):
    def __init__(self, input: Input):
        super().__init__()
        self.set_input(input)

    def set_input(self, input: Input):
        self._hls = input.media.hls(self.format)

    def set_representation(self, repr: Representation):
        self._hls.representations(repr)

    @property
    def format():
        return Formats.h264()

    def transcode(self, output_dir: str):
        self._hls.output(output_dir, monitor=progress)


class DASH(Codec):
    def __init__(self, input: Input):
        super().__init__()
        self.set_input(input)

    def set_input(self, input: Input):
        self._dash = input.media.dash(self.format)

    def set_representation(self, repr: Representation):
        self._dash.representations(repr)

    @property
    def format():
        return Formats.vp8()

    def transcode(self, output_dir: str):
        self._dash.output(output_dir, monitor=progress)
