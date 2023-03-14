from __future__ import annotations

from abc import abstractmethod, ABC
from src.sdk.harvest.model import Media
from src.core.types import (
    Path,
    URL,
    Union,
    Generic,
    T,
    Set,
    Setting,
)


# Alias for allowed engine inputs
Processable = Media[Union[Path, URL]]


class Engine(ABC, Generic[T]):
    """Engine implements a media engine template that uses an underlying library as interface to process media files and produce output.
    The engine adapt dynamically the library so that methods can be directly accessed and process media in a specific context.
    """

    _name: str
    _library: T
    _settings: Set[Setting]

    def __init__(self, name: str, input: T):
        """Initialize a new instance with bound library and name"""
        self._input = input
        self._name = name
        self._settings = set()

    def __str__(self):
        """String representation for library"""
        return self._name

    def configure(self, setting: Setting) -> Engine[T]:
        """Set the context for media processing.

        :param setting: the setting to bind
        :return: the self adapter
        :rtype: Adapter[Any]
        """

        self._settings.add(setting)
        return self

    @abstractmethod
    def save(self, path: Path) -> Media[Path]:
        """Store the new media based on configuration context.

        :param path: the output path
        :return: new media path
        :rtype: Media[Path]
        :raises ProcessingException: if any exception is captured during processing
        """
        ...
