from __future__ import annotations

from nucleus.core.types import Protocol, Settings


class Codec(Settings, Protocol):
    """Codec compression abstraction.
    ref: https://trac.ffmpeg.org/wiki/Encode/VP9
    ref: https://trac.ffmpeg.org/wiki/Encode/H.265
    ref: https://trac.ffmpeg.org/wiki/Encode/H.264
    """

    def __contains__(self, codec: str) -> bool:
        """Check if the available codecs contain the codec in question.
        If codec match we can just copy it.

        :para codec: the name of the codec to match
        :returns: true if match else False
        :rtype: bool
        """
        ...
