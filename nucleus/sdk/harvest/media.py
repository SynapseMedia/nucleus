from nucleus.core.types import URL, Path, Union

from .models import Media

"""
Each specification defines how media types are processed and stored.
The behavior of media types in the context of processing and storage is defined by each specification.
"""

# Alias for sources allowed to collect media
Collectable = Media[Union[URL, Path]]


class Video(Collectable):
    """Video class establishes how the videos should be processed"""

    ...


class Image(Collectable):
    """Image class establishes how the images should be processed"""

    ...


__all__ = (
    'Image',
    'Video',
)
