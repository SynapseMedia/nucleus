from __future__ import annotations

from abc import abstractmethod, ABC
from nucleus.sdk.harvest.model import Media
from nucleus.core.types import (
    T,
    Path,
    Iterator,
    URL,
    Union,
    Generic,
    Set,
    Tuple,
    Any,
    Setting,
)


# Alias for allowed engine inputs
Processable = Media[Union[Path, URL]]
Compiled = Iterator[Tuple[str, Any]]


class Engine(ABC, Generic[T]):
    """Engine implements a media engine adapter template that uses an underlying library as interface to process media files and produce output.
    The engine adapt dynamically the library so that methods can be directly accessed and process media in a specific context.
    Use this class to create engine subtypes.
    """

    _name: str
    _library: T
    _settings: Set[Setting]

    def __init__(self, name: str, lib: T):
        """Initialize a new instance with bound library and name"""
        self._name = name
        self._library = lib
        self._settings = set()

    def __str__(self):
        """String representation for library"""
        return self._name

    def compile(self) -> Compiled:
        """Join config as output map arguments"""
        for preset in self._settings:
            yield preset.__class__.__name__, dict(preset)

    def configure(self, setting: Setting) -> Engine[T]:
        """Set the context for media processing.

        :param setting: the setting to bind
        :return: the self adapter
        :rtype: Engine[T]
        """

        self._settings.add(setting)
        return self

    @abstractmethod
    def save(self, path: Path) -> Media[Path]:
        """Store the new media based on configuration context.

        :param path: the output path
        :return: new media path
        :rtype: Media[Path]
        :raises ProcessingEngineError: if any exception is captured during processing
        """
        ...
