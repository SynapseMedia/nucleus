import functools

from pydantic import ValidationError, create_model, parse_obj_as

from nucleus.core.types import Any, T, Type
from nucleus.sdk.exceptions import ModelValidationError

from .media import Image, Video
from .models import Model


def media_factory(*, base: Type[T], **kwargs: Any) -> T:
    """Generic model factory.
    Creates a new model based on the provided `base` model.

    Usage:

        # create our own media partial
        music = functools.partial(media_factory, base=Music)

    :param base: The base type for model
    :param **kwargs: The fields to declare into media model
    :return: New media type instance
    :raises ModelValidationError: If model fails during schema validation
    """
    try:
        return parse_obj_as(base, kwargs)
    except ValidationError as e:
        raise ModelValidationError(f'exceptions raised during schema validation in partials factory: {str(e)}')


# Extend the default Model base and use `create_model` from pydantic to create ready-to-use models.
# Learn more about `create_model` [here](https://docs.pydantic.dev/latest/usage/models/)
model = functools.partial(create_model, __base__=Model)
# We use utility functions to create "out of the box" media models derived from media types
image = functools.partial(media_factory, base=Image)
video = functools.partial(media_factory, base=Video)


__all__ = ('model', 'image', 'video')
