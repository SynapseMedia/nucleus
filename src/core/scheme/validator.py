from .definition import MovieScheme
from src.core import Log, logger
from marshmallow.exceptions import ValidationError


def check(data: list, many: bool = True, **kwargs) -> MovieScheme:
    """
    Bypass check data in scheme
    :param data: List of schemas object
    :param many: Validate many or a single object
    :return Validated schema
    """
    try:
        return MovieScheme(
            many=many, **kwargs
        ).load(data)
    except ValidationError as e:
        logger.error(f"{Log.FAIL}{e}{Log.ENDC}")
        exit(1)


__all__ = ['check']
