import functools
import nucleus.sdk.exceptions as exceptions

from nucleus.core.types import Any, Type
from pydantic import create_model, parse_obj_as, ValidationError

from .model import Meta, Collectable
from .media import Image, Video


def media_factory(base: Type[Collectable], **kwargs: Any) -> Collectable:
    """Enhanced parse obj to allow named parameters as obj

    :param base: the base type for model
    :return: new collectable model
    :rtype: Collectable
    :raises: ModelValidationError: if model fails during schema validation
    """
    try:
        return parse_obj_as(base, kwargs)
    except ValidationError as e:
        raise exceptions.ModelValidationError(
            f"exceptions raised during schema validation in partials factory: {str(e)}"
        )


# A partial prepared model factory functions
meta = functools.partial(create_model, __base__=Meta)
image = functools.partial(media_factory, base=Image)
video = functools.partial(media_factory, base=Video)


__all__ = ("meta", "image", "video")
