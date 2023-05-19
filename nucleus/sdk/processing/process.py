import functools

import ffmpeg
import PIL.Image as PIL

from nucleus.core.types import Path
from nucleus.sdk.harvest import Image, Video

from .engines import ImageEngine, VideoEngine
from .types import Engine, Processable


@functools.singledispatch
def engine(media: Processable) -> Engine:
    """Engine single dispatch factory.
    Use the media input to infer the right engine.

    :param media: the media to dispatch
    :param kwargs: these args are passed directly to library.
    :return: engine instance
    :rtype: Engine
    """
    raise NotImplementedError(f'cannot process not registered media `{media}')


@engine.register
def _(media: Video) -> VideoEngine:
    input_path = Path(media.path)
    library = ffmpeg.input(input_path)  # type: ignore
    return VideoEngine(library)  # type: ignore


@engine.register
def _(media: Image) -> ImageEngine:
    input_path = Path(media.path)
    library = PIL.open(input_path)
    return ImageEngine(library)


__all__ = ('engine',)
