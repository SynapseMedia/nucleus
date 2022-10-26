import src.core.cache as cache

# Convention for importing constants and types
from src.core.types import List
from src.core.cache.types import Connection, Cursor, Query
from .constants import INSERT_MOVIE
from .types import Movie, Media


def _query_from_media(media: Media):
    pass

def _query_from_movie(movie: Movie) -> Query:
    """Build a query based on movie
    
    :param movie: The movie to build query
    :return: Query ready to exec
    :rtype: Query
    
    """
    dict_movie = movie.dict(exclude={"resources"})
    movie_fields = ",".join(dict_movie.keys())
    # We generate a list of "?" to populate the query values
    # ref: https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor.execute
    escaped_values = ",".join(["?" for _ in range(len(dict_movie))])
    
    # Build query based on movie input data
    query = INSERT_MOVIE % (movie_fields, escaped_values)
    values =  dict_movie.values()
    return Query(query, list(values))


@cache.atomic
def freeze(conn: Connection, movie: Movie) -> bool:
    """Insert movies in metadata cache.

    :param movie: movie to store
    :return: True if successful, False otherwise
    :rtype: bool
    """

    # Build query based on movie input data
    query = _query_from_movie(movie)
    cursor: Cursor = cache.exec(query, conn=conn)
    movie_id = cursor.lastrowid

    resources: List[Media]  = movie.resources
    resources_map = map(lambda x: [movie_id, *dict(x).values()], resources)


    # TODO insert here resources after get the exec id
    # resources = 

    # resources = ... # use it to store resources
    # inserted = cache.batch(conn, INSERT_MOVIE, *movie)
    # return inserted > 0
    return False


def frozen() -> List[Movie]:
    """Return already stored movies
    :return: List of movies
    :rtype: List[Movies]
    """
    pass
