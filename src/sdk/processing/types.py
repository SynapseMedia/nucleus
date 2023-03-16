from __future__ import annotations

from abc import abstractmethod, ABC
from src.sdk.harvest.model import Media
from src.core.types import (
    T,
    Path,
    Iterator,
    URL,
    Union,
    Generic,
    Set,
    Setting,
    Tuple,
    Any,
)


# Alias for allowed engine inputs
Processable = Media[Union[Path, URL]]
Compiled = Iterator[Tuple[str, Any]]


class Engine(ABC, Generic[T]):
    """Engine implements a media engine adapter template to process media files and produce output.
    The engine adapt dynamically the library to process media in a specific context.
    """

    _name: str
    _library: T
    _settings: Set[Setting]

    def __init__(self, name: str, input: T):
        """Initialize a new instance with bound library and name"""
        self._name = name
        self._library = input
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
