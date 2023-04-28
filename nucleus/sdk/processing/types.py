from __future__ import annotations
from abc import abstractmethod, ABC
from nucleus.sdk.harvest import Media
from nucleus.core.types import (
    T,
    Path,
    Iterator,
    URL,
    Union,
    Generic,
    List,
    Tuple,
    Any,
    Setting,
    Dynamic,
)


# Alias for allowed engine inputs
Processable = Media[Union[Path, URL]]
Compilation = Iterator[Tuple[str, Any]]


class Introspection(Dynamic):
    """Introspection hold internal media information/metadata.
    For each result the media metadata is associated as `meta` and it could change based on media type and underneath library.

    eg.
        # could be related to ffprobe video info or PIL.Image, etc
        video = Introspection(**ffprobe)
        image = Introspection(**PIL.Image)

        # in this case introspection dynamically receive all the metadata from the underneath library output
        # the "WARNING" here is that based on media type the introspection content could change and needs an extra review.
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


class Engine(ABC, Generic[T]):
    """Engine implements a media engine adapter template that uses an underlying library as interface to process media files and produce output.
    The engine adapt dynamically the library so that methods can be directly accessed and process media in a specific context.
    Use this class to create engine subtypes.
    """

    _library: T
    _settings: List[Setting]

    def __init__(self, lib: T):
        """Initialize a new instance with bound library and name"""
        self._library = lib
        self._settings = list()

    def compile(self) -> Compilation:
        """Compile engine settings into an map of arguments

        :return: a new map of compiled arguments using
        :rtype: Compilation
        """
        for preset in self._settings:
            yield type(preset).__name__, dict(preset)

    def configure(self, setting: Setting) -> Engine[T]:
        """Set the context for media processing.

        :param setting: the setting to bind
        :return: the self adapter
        :rtype: Engine[T]
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
        """Store the new media based on configuration context.

        :param path: the output path
        :return: new media path
        :rtype: File
        :raises ProcessingEngineError: if any exception is captured during processing
        """
        ...
