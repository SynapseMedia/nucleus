import functools

import ffmpeg
import PIL.Image as PIL

from nucleus.core.types import Path,URL,    Path,    Union
from nucleus.sdk.harvest import Image, Video, Media

from .engines import ImageEngine, VideoEngine
from .types import Engine


@functools.singledispatch
def engine(media: Media[Union[Path, URL]]) -> Engine:
    """Engine singledispatch factory.
    Use the media input to infer the right engine.

    :param media: The media type to dispatch
    :return: The appropriate engine implementation for the type of media
    """
    raise NotImplementedError(f'cannot process not registered media `{media}')


@engine.register
def _(media: Video) -> VideoEngine:
    input_path = Path(media.path)
    library = ffmpeg.input(input_path)
    return VideoEngine(library)


@engine.register
def _(media: Image) -> ImageEngine:
    input_path = Path(media.path)
    library = PIL.open(input_path)
    return ImageEngine(library)


__all__ = ('engine',)
