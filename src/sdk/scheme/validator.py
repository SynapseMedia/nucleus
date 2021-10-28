from typing import Iterator
from marshmallow import EXCLUDE
from marshmallow.exceptions import ValidationError
from .definition.movies import MovieScheme
from .. import logger


def parse(mv_list: list) -> Iterator[MovieScheme]:
    """
    Parse MovieScheme list [dict => MovieSchemeObject]
    :param mv_list: list of MovieScheme dicts
    """
    movie_scheme = MovieScheme(unknown=EXCLUDE)
    for mv in mv_list:
        yield movie_scheme.load(mv)


def check(data: list, many: bool = True, **kwargs) -> MovieScheme:
    """
    Bypass check data in scheme
    :param data: List of schemas object
    :param many: Validate many or a single object
    :raise ValidationError
    :return Validated schema
    """
    try:
        return MovieScheme(many=many, **kwargs).load(data)
    except ValidationError as e:
        logger.log.error(f"{e}")
        exit(1)


__all__ = ["check", "parse"]
