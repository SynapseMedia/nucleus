from __future__ import annotations

from abc import abstractmethod
from src.core.types import Protocol as P, Setting


class Codec(Setting, P):
    """Codec compression abstraction.
    ref: https://trac.ffmpeg.org/wiki/Encode/VP9
    ref: https://trac.ffmpeg.org/wiki/Encode/H.265
    ref: https://trac.ffmpeg.org/wiki/Encode/H.264
    """

    @abstractmethod
    def __contains__(self, codec: str) -> bool:
        """Check if the available codecs contain the codec in question.
        If codec match we can just copy it.

        :para codec: the name of the codec to match
        :returns: true if match else False
        :rtype: bool
        """
        ...


class Option(Setting, P):
    """The option class defines a generic controller for the behavior of ffmpeg options
    depending on how the action is determined as either input or output of the command.
    ref: https://ffmpeg.org/ffmpeg.html#Main-options

    """

    ...


class Protocol(Setting, P):
    """Streaming protocol abstraction.
    ref: https://en.wikipedia.org/wiki/HTTP_Live_Streaming
    ref: https://en.wikipedia.org/wiki/Dynamic_Adaptive_Streaming_over_HTTP
    ref: https://ffmpeg.org/ffmpeg-formats.html#Options-10
    ref: https://ffmpeg.org/ffmpeg-formats.html#dash-2
    """

    ...


__all__ = ()
