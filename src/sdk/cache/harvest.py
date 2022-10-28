import src.core.cache as cache

# Convention for importing constants and types
from src.core.types import List
from src.core.cache.types import Connection, Cursor, Query
from .types import Movie


@cache.atomic
def freeze(conn: Connection, movie: Movie) -> bool:
    """Insert movies in metadata cache.

    :param movie: movie to store
    :return: True if successful, False otherwise
    :rtype: bool
    """

    # Build query based on movie input data
    query: Query = movie.create.write()
    cursor: Cursor = conn.execute(query.sql, query.values)
    return cursor.rowcount > 0


def frozen() -> List[Movie]:
    """Return already stored movies

    :return: List of movies
    :rtype: List[Movies]
    """
    # TODO yield here movies
    return []
