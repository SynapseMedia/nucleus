from src.sdk.harvest import Video, Image
from src.sdk.harvest.types import Media
from functools import singledispatch

# from .types import Engine


@singledispatch
def process(model: Media):
    raise NotImplementedError()


@process.register
def _(model: Video):
    ...


@process.register
def _(model: Image):
    ...
