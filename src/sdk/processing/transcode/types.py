from __future__ import annotations

from enum import Enum
from abc import ABCMeta, abstractmethod
from src.core.types import Any, Protocol as P, Iterator, Tuple, Iterable
from ffmpeg.nodes import FilterableStream as FFMPEG, OutputNode as Spec  # type: ignore

Preset = Tuple[str, Any]
Settings = Iterable[Iterator[Preset]]


class Operations(Enum):
    IN = 0
    OUT = 1


class Option(P, metaclass=ABCMeta):
    """The option class defines a generic controller for the behavior of ffmpeg options
    depending on how the action is determined as either input or output of the command.
    ref: https://ffmpeg.org/ffmpeg.html#Main-options

    """

    @abstractmethod
    def __contains__(self, op: Operations) -> bool:
        """Check if option allowed for input/output operation

        :param op: should be the check to expected operation
        :return: True if option is allowed for input/output operation
        :rtype: bool
        """
        ...

    @abstractmethod
    def __iter__(self) -> Iterator[Preset]:
        """Yield key value pair to build ffmpeg arguments.
        Allow to convert option as dict since constructor accept key value iterable pair"""


class Codec(P, metaclass=ABCMeta):
    """Codec compression abstraction.
    ref: https://trac.ffmpeg.org/wiki/Encode/VP9
    ref: https://trac.ffmpeg.org/wiki/Encode/H.265
    ref: https://trac.ffmpeg.org/wiki/Encode/H.264
    """

    @abstractmethod
    def __iter__(self) -> Iterator[Preset]:
        """Yield key value pair codec arguments"""
        ...

    @abstractmethod
    def __contains__(self, codec: str) -> bool:
        """Check if the available codecs contain the codec in question.
        If codec match we can just copy it.

        :para codec: the name of the codec to match
        :returns: True if match else False
        :rtype: bool
        """
        ...


class Protocol(P, metaclass=ABCMeta):
    """Streaming protocol abstraction.
    ref: https://en.wikipedia.org/wiki/HTTP_Live_Streaming
    ref: https://en.wikipedia.org/wiki/Dynamic_Adaptive_Streaming_over_HTTP
    ref: https://ffmpeg.org/ffmpeg-formats.html#Options-10
    ref: https://ffmpeg.org/ffmpeg-formats.html#dash-2
    """

    @abstractmethod
    def __iter__(self) -> Iterator[Preset]:
        """Yield key value pair protocol arguments"""
        ...


__all__ = ("FFMPEG", "Spec", "Preset", "Codec", "Protocol")
