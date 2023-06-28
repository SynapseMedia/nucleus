from nucleus.core.types import Literal

from .constants import (
    DEFAULT_AUDIO_CODEC,
    DEFAULT_CRF,
    DEFAULT_GOP,
    DEFAULT_KEY_MIN,
    DEFAULT_SC_THRESHOLD,
)


class Copy:
    """Used to `copy` the codec from the source to the output.
    Special value copy (output only) to indicate that the stream is not to be re-encoded.

    Usage:

        copy_audio_stream = Copy("a")
        copy_video_stream = Copy("v")
    """

    _stream_specifier: str

    def __init__(self, stream: Literal['v', 'a'] = 'v'):  # noqa: F821
        self._stream_specifier = stream

    def __contains__(self, codec: str) -> bool:
        ...

    def __iter__(self):
        yield f'c:{self._stream_specifier}', 'copy'


class H264:
    """Represents a H264 codec.

    Usage:

        h264 = H264()

    """

    def __contains__(self, codec: str) -> bool:
        videos = ['libx264', 'h264', 'h264_afm', 'h264_nvenc']
        audios = ['aac', 'libvo_aacenc', 'libfaac', 'libmp3lame', 'libfdk_aac']
        allowed_codecs = videos + audios
        return codec in allowed_codecs

    def __iter__(self):
        yield 'bf', 1
        yield 'g', DEFAULT_GOP
        yield 'crf', DEFAULT_CRF
        yield 'keyint_min', DEFAULT_KEY_MIN
        yield 'sc_threshold', DEFAULT_SC_THRESHOLD
        yield 'c:a', DEFAULT_AUDIO_CODEC
        yield 'c:v', 'libx264'


class HEVC:
    """Represents a HEVC codec.

    Usage:

        hevc = HEVC()

    """

    def __contains__(self, codec: str) -> bool:
        videos = ['libx265', 'h265']
        audios = ['aac', 'libvo_aacenc', 'libfaac', 'libmp3lame', 'libfdk_aac']
        allowed_codecs = videos + audios
        return codec in allowed_codecs

    def __iter__(self):
        yield 'g', DEFAULT_GOP
        yield 'crf', DEFAULT_CRF
        yield 'keyint_min', DEFAULT_KEY_MIN
        yield 'sc_threshold', DEFAULT_SC_THRESHOLD
        yield 'c:a', DEFAULT_AUDIO_CODEC
        yield 'c:v', 'libx265'
        yield 'x265-params', 'lossless=1'


class VP9:
    """Represents a VP9 codec.

    Usage:

        vp9 = VP9()

    """

    def __contains__(self, codec: str) -> bool:
        videos = ['libvpx', 'libvpx-vp9']
        audios = ['aac', 'libvo_aacenc', 'libfaac', 'libmp3lame', 'libfdk_aac']
        allowed_codecs = videos + audios
        return codec in allowed_codecs

    def __iter__(self):
        yield 'c:a', DEFAULT_AUDIO_CODEC
        yield 'c:v', 'libvpx-vp9'


__all__ = ('HEVC', 'VP9', 'H264', 'Copy')
