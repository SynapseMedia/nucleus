import ffmpeg  # type: ignore
import PIL.Image as PIL
import src.sdk.processing.image as image
import src.sdk.processing.video as video

from ffmpeg.nodes import FilterableStream as FFMPEG  # type: ignore
from PIL.Image import Image as Pillow

from functools import singledispatch
from src.core.types import Any, Path
from src.sdk.harvest import Video as VideoModel, Image as ImageModel

from .engines import Video, Image
from .types import Engine, Processable


@singledispatch
def engine(model: Processable, **kwargs: Any) -> Engine[Any]:
    """Engine single dispatch factory.
    Use the model input to infer the right engine.

    :param model: the model to dispatch
    :param kwargs: these args are passed directly to library.
    :return: Engine instance
    :rtype: Engine
    """
    raise NotImplementedError(f"cannot process not registered media `{model}")


@engine.register
def _(model: VideoModel, **kwargs: Any) -> Video:
    input_path = Path(model.route)
    library: FFMPEG = ffmpeg.input(input_path, **kwargs)  # type: ignore
    # Adapter for FFMPEG video lib
    adapter = video.FFMPEG(model.type, library)
    return Video(adapter)


@engine.register
def _(model: ImageModel, **kwargs: Any) -> Image:
    input_path = Path(model.route)
    library: Pillow = PIL.open(input_path, **kwargs)
    # Adapter for Pillow image lib
    adapter = image.Pillow(model.type, library)
    return Image(adapter)
