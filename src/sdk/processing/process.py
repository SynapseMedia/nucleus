from functools import singledispatch
from src.sdk.harvest import (
    Video as VideoModel,
    Image as ImageModel,
    Stream as StreamModel,
)

from .engines import Video, Image, Stream
from .types import Engine, Processable


@singledispatch
def engine(model: Processable) -> Engine:
    raise NotImplementedError(f"cannot process not registered media `{model}")


@engine.register
def _(model: VideoModel) -> Video:
    return Video(model)


@engine.register
def _(model: StreamModel) -> Stream:
    return Stream(model)


@engine.register
def _(model: ImageModel) -> Image:
    return Image(model)
