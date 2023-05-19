from __future__ import annotations

from abc import ABC, abstractmethod

from nucleus.core.types import (
    URL,
    Any,
    Dynamic,
    Iterator,
    List,
    Path,
    Settings,
    Tuple,
    Union,
)
from nucleus.sdk.harvest import Media

# Alias for allowed engine inputs
Processable = Media[Union[Path, URL]]
Compilation = Iterator[Tuple[str, Any]]


class Introspection(Dynamic):
    """Introspection hold internal media information/metadata.
    For each result the media metadata is associated as `meta` and it could change
    based on media type and underneath library.

    eg.
        # could be related to ffprobe video info or PIL.Image, etc
        video = Introspection(**ffprobe)
        image = Introspection(**PIL.Image)

        # in this case introspection dynamically receive all the metadata from the underneath library output
        # the "WARNING" here is that based on media type
        # the introspection content could change and needs an extra review.
    """

    size: int
    # we expect to fill this field with IANA Media types
    # https://www.iana.org/assignments/media-types/media-types.xhtml
    type: str


class File(Media[Path]):
    """Local media file representation.
    This class is used to infer any media stored in local host.
    """

    # associated file introspection
    meta: Introspection
    ...


class Engine(ABC):
    """Engine implements a media engine template/adapter.
    It uses an underlying library as an interface to process media files.
    It produce output based on the provided settings.
    Use this class to create engine subtypes.
    """

    _library: Any
    _settings: List[Settings]

    def __init__(self, lib: Any):
        """Initialize a new instance with bound library"""
        self._library = lib
        self._settings = []

    def compile(self) -> Compilation:
        """Compile engine settings into an map of arguments

        :return: a new map of compiled arguments using
        :rtype: Compilation
        """
        for preset in self._settings:
            yield type(preset).__name__, dict(preset)

    def configure(self, setting: Settings) -> Engine:
        """Set the context for media processing.

        :param setting: the setting to bind
        :return: the self adapter
        :rtype: Engine
        """

        self._settings.append(setting)
        return self

    @abstractmethod
    def introspect(self, path: Path) -> Introspection:
        """Return technical information of the input media.

        :param path: the media path if None the internal media is evaluated
        :return: any technical information collected from media.
        :rtype: Introspection object
        """
        ...

    @abstractmethod
    def save(self, path: Path) -> File:
        """Store the new media based on conf context and bounded library.

        :param path: the output path
        :return: new media path
        :rtype: File
        :raises ProcessingEngineError: if any exception is captured during processing
        """
        ...


__all__ = ('Engine', 'File', 'Introspection')
