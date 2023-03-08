import src.sdk.exceptions as exceptions

from .types import Preset
from .constants import (
    HLS_TIME,
    HLS_LIST_SIZE,
    HLS_PLAYLIST_TYPE,
    HLS_CODEC,
    HLS_CODEC_PARAMS,
    HLS_TAG_VIDEO_FORMAT,
)


def _hls() -> Preset:
    """Presets for HLS streaming protocol.
    Could be overridden by engine output kwargs options.

    ref: https://developer.apple.com/documentation/http_live_streaming/http_live_streaming_hls_authoring_specification_for_apple_devices
    """
    return {
        "c:v": HLS_CODEC,
        "f": "hls",
        "x265-params": HLS_CODEC_PARAMS,
        "hls_time": HLS_TIME,
        "hls_list_size": HLS_LIST_SIZE,
        "hls_playlist_type": HLS_PLAYLIST_TYPE,
        "tag:v": HLS_TAG_VIDEO_FORMAT,
    }


def _dash() -> Preset:
    return {}


def protocol(ext: str) -> Preset:
    """Return the streaming protocol preset related to the given file extension.

    :param format: the streaming protocol file extension
    :return: preset from the given file extension
    :rtype: Preset
    :raises ProcessingException: if not preset found
    """

    presets = {
        "m3u8": _hls,
        "mpd": _dash,
    }

    if ext not in presets:
        raise exceptions.ProcessingException(
            f"not supported output file format {ext}")
    return presets[ext]()
