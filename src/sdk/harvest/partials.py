import functools

from src.core.types import Any, Type
from pydantic import create_model, parse_obj_as

from .model import Meta, Collectable
from .media import Image, Video, Stream


def media_factory(base: Type[Collectable], **kwargs: Any) -> Collectable:
    """Enhanced parse obj to allow named parameters as obj"""
    return parse_obj_as(base, kwargs)


# A partial prepared model factory functions
meta = functools.partial(create_model, __base__=Meta)
image = functools.partial(media_factory, base=Image)
video = functools.partial(media_factory, base=Video)
stream = functools.partial(media_factory, base=Stream)


__all__ = ("meta", "image", "video", "stream")
