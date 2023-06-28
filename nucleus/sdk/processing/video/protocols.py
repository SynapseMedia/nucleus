from dataclasses import dataclass

from .codecs import H264
from .constants import HLS_LIST_SIZE, HLS_PLAYLIST_TYPE, HLS_TAG_VIDEO_FORMAT, HLS_TIME
from .types import Codec


@dataclass(slots=True)
class HLS:
    """Represents a HLS streaming protocol.

    Usage:

        # use h264 as codec
        hls = HLS(H264())

    """

    # default h264 codec
    codec: Codec = H264()

    def __iter__(self):
        yield 'hls_time', HLS_TIME
        yield 'hls_list_size', HLS_LIST_SIZE
        yield 'hls_playlist_type', HLS_PLAYLIST_TYPE,
        yield 'tag:v', HLS_TAG_VIDEO_FORMAT,
        yield from self.codec


__all__ = ('HLS',)
