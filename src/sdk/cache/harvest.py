import src.core.cache as cache

# Convention for importing constants and types
from src.core.types import List
from src.core.cache.types import Connection, Cursor, Field
from .types import Movie


@cache.atomic
def freeze(conn: Connection, movie: Movie) -> bool:
    """Insert movies in metadata cache.

    :param movie: movie to store
    :return: True if successful, False otherwise
    :rtype: bool
    """

    # Build query based on movie input data
    query = movie.write(exclude={"resources"})
    cursor: Cursor = conn.execute(query.sql, query.values)

    # Movie + resources association
    movie_resources = movie.resources
    movie_field = Field("movie_id", cursor.lastrowid)
    movie_queries = map(lambda x: x.aggregate(movie_field).write(), movie_resources)
    
    # run movie resource queries
    expected_resources = len(movie_resources)
    cursors = map(lambda x: conn.execute(x.sql, x.values), movie_queries)
    batch_success = map(lambda c: c.rowcount == expected_resources, cursors)
    return all(batch_success)


def frozen() -> List[Movie]:
    """Return already stored movies

    :return: List of movies
    :rtype: List[Movies]
    """
    return []
