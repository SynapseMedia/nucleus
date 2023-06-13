from nucleus.core.types import URL, Path, Union

from .models import Media


class Video(Media[Union[URL, Path]]):
    """Represents a video media type."""

    ...


class Image(Media[Union[URL, Path]]):
    """Represents an image media type."""

    ...


__all__ = (
    'Image',
    'Video',
)
