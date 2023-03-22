import ffmpeg  # type: ignore
import PIL.Image as PIL

from functools import singledispatch
from nucleus.core.types import Any, Path
from nucleus.sdk.harvest import Video as VideoModel, Image as ImageModel

from .engines import Video, Image
from .types import Engine, Processable


@singledispatch
def engine(model: Processable) -> Engine[Any]:
    """Engine single dispatch factory.
    Use the model input to infer the right engine.

    :param model: the model to dispatch
    :param kwargs: these args are passed directly to library.
    :return: engine instance
    :rtype: Engine
    """
    raise NotImplementedError(f"cannot process not registered media `{model}")


@engine.register
def _(model: VideoModel) -> Video:
    input_path = Path(model.route)
    library = ffmpeg.input(input_path)  # type: ignore
    return Video(model.type, library)  # type: ignore


@engine.register
def _(model: ImageModel) -> Image:
    input_path = Path(model.route)
    library = PIL.open(input_path)
    return Image(model.type, library)


__all__ = ("engine",)
