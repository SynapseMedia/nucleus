from src.sdk.scheme.definition.movies import MovieScheme
from src.sdk import cache, logger, media, scheme


def boot(current_movie: MovieScheme):
    """
    Boot storage ingest process from metadata definition scheme
    :param current_movie: MovieScheme
    """
    _id = current_movie.imdb_code  # Current id
    # 1 - Add ingested directory hash to movie
    # 2 - Fit scheme from dag resources paths
    # 3 - Store in cursor db current processed movie
    current_movie.hash = media.storage.ingest.to_ipfs(current_movie)
    current_movie.resource = scheme.util.fit_resources_from_dag(current_movie.hash)
    cache.ingest.freeze(_id, MovieScheme().dump(current_movie))
    logger.log.success(f"Done {current_movie.imdb_code}\n")
