from src.sdk import media, logger, util
from src.sdk.scheme.definition.movies import MovieScheme


def boot(current_movie: MovieScheme):
    """
    Boot w3 metadata ERC1155 generation
    :param current_movie: MovieScheme
    """
    # Build metadata for current movie
    logger.log.warning(f"Processing NFT meta for {current_movie.imdb_code}")
    nft_movie_meta = media.metadata.generate_erc1155(current_movie)
    # Get directory output for current movie meta json
    current_dir = util.build_dir(current_movie)
    directory, _ = util.resolve_root_for(current_dir)
    # Write erc1155 to output dir
    util.write_json(f"{directory}/index.json", nft_movie_meta)
    logger.log.success(f"Written metadata for {current_movie.imdb_code}\n")
