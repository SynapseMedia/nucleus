from src.sdk.harvest import Media
from functools import singledispatch

# from .types import Engine


class Video:
    ...


class Image:
    ...


@singledispatch
def process(model: Media):
    raise NotImplementedError()


@process.register
def _(model: Video):
    ...


@process.register
def _(model: Image):
    ...
