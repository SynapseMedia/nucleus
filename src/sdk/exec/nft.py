from src.sdk.scheme.definition.movies import MovieScheme
from src.sdk import logger
from src.sdk.web3 import nft


def boot(current_movie: MovieScheme):
    """
    Boot nft initial holder process from metadata definition scheme
    :param current_movie: MovieScheme
    """
    nft.set_holder(current_movie.hash, current_movie.creator)
    logger.log.success(
        f"Done set holder as "
        f"{current_movie.creator} "
        f"for {current_movie.imdb_code}\n"
    )
