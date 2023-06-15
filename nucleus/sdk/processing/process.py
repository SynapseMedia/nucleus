import functools

import ffmpeg
import PIL.Image as PIL

from nucleus.core.types import Path
from nucleus.sdk.harvest import Image, Media, Video
from nucleus.sdk.exceptions import ProcessingEngineError
from .engines import ImageEngine, VideoEngine
from .types import Engine


@functools.singledispatch
def engine(media: Media[Path]) -> Engine:
    """Engine singledispatch factory.
    Use the media input to infer the right engine.
    
    Usage:
    
        # initialize an Image type to pass into engine function
        image = harvest.image(path=Path("image.jpg"))
        # get back an Image engine from the input type
        engine = processing.engine(image)

    :param media: The media type to dispatch
    :return: The appropriate engine implementation for the type of media
    :raises: ProcessingEngineError:  If any error occurs during engine initialization
    

    """
    raise NotImplementedError(f'cannot process not registered media `{media}')


@engine.register
def _(media: Video) -> VideoEngine:
    
    if not media.path.exists():
        raise ProcessingEngineError(f"No such file or directory: {media.path}")
    
    library = ffmpeg.input(media.path)
    return VideoEngine(library)

@engine.register
def _(media: Image) -> ImageEngine:
    try:
        library = PIL.open(media.path)
        return ImageEngine(library)
    except FileNotFoundError as e:
        raise ProcessingEngineError(str(e))

__all__ = ('engine',)
