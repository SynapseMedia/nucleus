import sys
import datetime

from ffmpeg_streaming import Representation, Formats  # type: ignore
from src.core.types import Directory

# package types
from .types import Streaming, Input


def output(_, duration: int, time_: int, time_left: int):
    """Render tqdm progress bar."""
    sys.stdout.flush()
    per = round(time_ / duration * 100)
    sys.stdout.write(
        "\rTranscoding...(%s%%) %s left [%s%s]"
        % (
            per,
            datetime.timedelta(seconds=int(time_left)),
            "#" * per,
            "-" * (100 - per),
        )
    )


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
        self._hls.output(output_dir, monitor=output)


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
        self._dash.output(output_dir, monitor=output)
