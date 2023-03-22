import functools

from nucleus.core.types import Any, Type
from pydantic import create_model, parse_obj_as

from .model import Meta, Collectable
from .media import Image, Video


def media_factory(base: Type[Collectable], **kwargs: Any) -> Collectable:
    """Enhanced parse obj to allow named parameters as obj"""
    return parse_obj_as(base, kwargs)


# A partial prepared model factory functions
meta = functools.partial(create_model, __base__=Meta)
image = functools.partial(media_factory, base=Image)
video = functools.partial(media_factory, base=Video)


__all__ = ("meta", "image", "video")
