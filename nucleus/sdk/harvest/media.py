from nucleus.core.types import Path

from .models import Media


class Video(Media[Path]):
    """Represents a video media type."""

    ...


class Image(Media[Path]):
    """Represents an image media type."""

    ...


__all__ = (
    'Image',
    'Video',
)
