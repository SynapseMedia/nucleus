import src.core.cache as cache

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

    
    
    insert = map(lambda x: tuple(x.dict().values()), data)
    # TODO insert the resources and genres here too
    inserted = cache.batch(conn, INSERT_MOVIE, *insert)
    return inserted > 0


def frozen() -> List[Movies]:
    """Return already stored movies
    :return: List of movies
    :rtype: List[Movies]
    """
    pass
