from typing import Iterator
from marshmallow import EXCLUDE
from marshmallow.exceptions import ValidationError
from .definition.movies import MovieScheme
from .. import logger


def check(data: list, many: bool = True, **kwargs) -> Iterator[MovieScheme]:
    """
    Bypass check data in scheme
    :param data: List of schemas object
    :param many: Validate many or a single object
    :raise ValidationError
    :return Validated schema
    """
    try:
        return MovieScheme(many=many, unknown=EXCLUDE, **kwargs).load(data)
    except ValidationError as e:
        logger.log.error(f"{e}")
        exit(1)


__all__ = ["check"]
