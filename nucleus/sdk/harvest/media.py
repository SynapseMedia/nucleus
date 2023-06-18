from nucleus.core.types import Path

from .models import Media


class Video(Media[Path]):
    """Represents a video media type.

    Usage:

        # create a new video type
        video = Video(path=Path("video.mp4"))

    """

    ...


class Image(Media[Path]):
    """Represents an image media type.

    Usage:

        # create a new image type
        image = Image(path=Path("image.jpg"))


    """

    ...


__all__ = (
    'Image',
    'Video',
)
