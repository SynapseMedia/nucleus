from __future__ import annotations

from abc import ABC, abstractmethod

from nucleus.core.types import Any, Dynamic, Iterator, List, Path, Settings, Tuple
from nucleus.sdk.harvest import Media


class Introspection(Dynamic):
    """Introspection holds internal media information and technical details from media resources.
    The media introspection may vary based on the media type and underlying library.

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

    Usage:

        # Introspect from ffprobe video info or PIL.Image, etc.
        video_meta = Introspection(**ffprobe)

        # create a local file with metadata information
        file = File(Path("local_video.mp4"), video_meta)

    """

    # associated file introspection
    meta: Introspection
    ...


class Engine(ABC):
    """Engine implements a media engine adapter.
    It uses an underlying library as an interface to process media files.
    It produce output based on the provided settings.
    """

    _library: Any
    _settings: List[Settings]

    def __init__(self, lib: Any):
        """Initialize a new instance with bound library

        :param lib: Any underlying lib
        """
        self._library = lib
        self._settings = []

    def compile(self) -> Iterator[Tuple[str, Any]]:
        """Compile engine settings into an map of arguments

        :return: A new map of compiled arguments based on settings
        """
        for preset in self._settings:
            yield type(preset).__name__, dict(preset)

    def configure(self, setting: Settings) -> Engine:
        """Add setting to media processing context

        :param setting: The setting to apply to the engine output.
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
        """Store the new media based on settings and bound library.

        :param path: The output path
        :return: File object
        :raises ProcessingEngineError: If any exception is captured during processing
        """
        ...


__all__ = ('Engine', 'File', 'Introspection')
