import src.core.cache as cache

from src.core.types import List
from .types import Movies


@cache.atomic
def freeze(data: List[Movies]):
    """Insert movies in metadata cache.

    :param data: list of movies to store
    :return: True if successful, False otherwise
    :rtype: bool
    """

    pass


def frozen() -> List[Movies]:
    """Return already stored movies
    :return: List of movies
    :rtype: List[Movies]
    """

    pass
