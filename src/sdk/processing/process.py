from functools import singledispatch

from src.sdk.harvest import Video, Image, Stream

from .engines import VideoEngine, ImageEngine, StreamEngine
from .types import Engine, Processable


@singledispatch
def engine(model: Processable) -> Engine:
    raise NotImplementedError(f"cannot process not registered media `{model}")


@engine.register
def _(model: Video) -> VideoEngine:
    return VideoEngine(model)


@engine.register
def _(model: Stream) -> StreamEngine:
    return StreamEngine(model)


@engine.register
def _(model: Image) -> ImageEngine:
    return ImageEngine(model)
