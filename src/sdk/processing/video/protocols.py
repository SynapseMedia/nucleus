from src.core.types import Setting

from .types import Codec
from .constants import HLS_TIME, HLS_PLAYLIST_TYPE, HLS_TAG_VIDEO_FORMAT, HLS_LIST_SIZE


class HLS(Setting):
    """Represent HLS streaming protocol.
    ref: https://ffmpeg.org/ffmpeg-formats.html#Options-10
    ref: https://en.wikipedia.org/wiki/HTTP_Live_Streaming

    """

    _codec: Codec

    def __init__(self, codec: Codec):
        self._codec = codec

    def __iter__(self):
        yield "hls_time", HLS_TIME
        yield "hls_list_size", HLS_LIST_SIZE
        yield "hls_playlist_type", HLS_PLAYLIST_TYPE,
        yield "tag:v", HLS_TAG_VIDEO_FORMAT,
        yield from self._codec


__all__ = ("HLS",)
