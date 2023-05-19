import functools

from pydantic import ValidationError, create_model, parse_obj_as

from nucleus.core.types import Any, T, Type
from nucleus.sdk.exceptions import ModelValidationError

from .media import Image, Video
from .models import Model


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
        raise ModelValidationError(f'exceptions raised during schema validation in partials factory: {str(e)}')


# A partial prepared model factory functions
model = functools.partial(create_model, __base__=Model)
image = functools.partial(media_factory, base=Image)
video = functools.partial(media_factory, base=Video)


__all__ = ('model', 'image', 'video')
