import functools

from nucleus.core.types import Any, Type, T
from pydantic import create_model, parse_obj_as, ValidationError
from nucleus.sdk.exceptions import ModelValidationError

from .models import Model
from .media import Image, Video


def media_factory(*, base: Type[T], **kwargs: Any) -> T:
    """Enhanced parse obj to allow named parameters as obj

    :param base: the base type for model
    :return: new collectable model
    :rtype: Collectable
    :raises: ModelValidationError: if model fails during schema validation
    """
    try:
        return parse_obj_as(base, kwargs)
    except ValidationError as e:
        raise ModelValidationError(
            f"exceptions raised during schema validation in partials factory: {str(e)}"
        )


# A partial prepared model factory functions
meta = functools.partial(create_model, __base__=Model)
image = functools.partial(media_factory, base=Image)
video = functools.partial(media_factory, base=Video)


__all__ = ("meta", "image", "video")
