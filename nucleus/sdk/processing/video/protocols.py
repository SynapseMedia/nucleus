from dataclasses import dataclass

from .constants import HLS_LIST_SIZE, HLS_PLAYLIST_TYPE, HLS_TAG_VIDEO_FORMAT, HLS_TIME
from .types import Codec


@dataclass(slots=True)
class HLS:
    """Represent HLS streaming protocol.
    ref: https://ffmpeg.org/ffmpeg-formats.html#Options-10
    ref: https://en.wikipedia.org/wiki/HTTP_Live_Streaming

    """

    codec: Codec

    def __iter__(self):
        yield 'hls_time', HLS_TIME
        yield 'hls_list_size', HLS_LIST_SIZE
        yield 'hls_playlist_type', HLS_PLAYLIST_TYPE,
        yield 'tag:v', HLS_TAG_VIDEO_FORMAT,
        yield from self.codec


__all__ = ('HLS',)
