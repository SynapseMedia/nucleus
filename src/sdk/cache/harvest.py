import src.core.cache as cache

# Convention for importing constants and types
from src.core.types import List
from src.core.cache.types import Connection
from .constants import INSERT_MOVIE
from .types import Movies


@cache.atomic
def freeze(conn: Connection, data: List[Movies]) -> bool:
    """Insert movies in metadata cache.

    :param data: list of movies to store
    :return: True if successful, False otherwise
    :rtype: bool
    """

    # TODO here need to split resources first
    movie = map(lambda x: x.dict(exclude={"resources"}).values(), data)
    resources = ... # use it to store resources
    inserted = cache.batch(conn, INSERT_MOVIE, *movie)
    return inserted > 0


def frozen() -> List[Movies]:
    """Return already stored movies
    :return: List of movies
    :rtype: List[Movies]
    """
    pass
