import click
from src.sdk.scheme.validator import check
from src.sdk import cache, media, exception, logger, util


@click.group("meta")
def nft():
    """
    NFT tools
    """
    pass


@nft.command()
def generate():
    """Generate metadata json file for ERC1155 NFT"""
    # Return available and not processed entries
    # Total size of entries to fetch
    result, result_count = cache.retrieve()

    if result_count == 0:  # If not data to fetch
        raise exception.EmptyCache()

    # Generate metadata file from each row in tmp db the resources
    for current_movie in check(result):
        logger.log.warning(f"Processing NFT meta for {current_movie.imdb_code}")
        # Build metadata for current movie
        nft_movie_meta = media.nft.erc1155_metadata(current_movie)
        # Get directory output for current movie meta json
        current_dir = util.build_dir(current_movie)
        directory, _ = util.resolve_root_for(current_dir)
        util.write_json(f"{directory}/index.json", nft_movie_meta)
        logger.log.success(f"Written metadata for {current_movie.imdb_code}\n")
