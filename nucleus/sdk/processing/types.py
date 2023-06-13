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
    """Introspection holds internal media information and metadata.
    For each result, the media metadata is associated with the `meta` attribute, and it could change
    based on the media type and underlying library.

    Usage:

        # Introspect from ffprobe video info or PIL.Image, etc.
        video = Introspection(**ffprobe)
        image = Introspection(**PIL.Image)

        # Introspection dynamically receives all the metadata from the underlying library output.
        # The "WARNING" here is that based on the media type,
        # the introspection content could change and requires an extra review.
    """

    size: int
    # We expect to fill this field with IANA Media types
    # https://www.iana.org/assignments/media-types/media-types.xhtml
    type: str


class File(Media[Path]):
    """Local media file representation.
    This class is used to represent any media stored in local host.
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

        :return: A new map of compiled arguments based on configured options
        """
        for preset in self._settings:
            yield type(preset).__name__, dict(preset)

    def configure(self, setting: Settings) -> Engine:
        """Set the context for media processing

        :param setting: The settings to apply to the engine output.
        :return: Engine object
        """

        self._settings.append(setting)
        return self

    @abstractmethod
    def introspect(self, path: Path) -> Introspection:
        """Return technical information of the input media.

        :param path: The media path
        :return: Any technical information collected from media.
        """
        ...

    @abstractmethod
    def save(self, path: Path) -> File:
        """Store the new media based on conf context and bound library.

        :param path: The output path
        :return: File object
        :raises ProcessingEngineError: If any exception is captured during processing
        """
        ...


__all__ = ('Engine', 'File', 'Introspection')
