import click

import os
from src.sdk.scheme.validator import check
from src.sdk import cache, media, logger, exception, util

OVERWRITE_TRANSCODE_OUTPUT = os.getenv("OVERWRITE_TRANSCODE_OUTPUT", "False") == "True"


@click.command()
@click.option("--overwrite", default=OVERWRITE_TRANSCODE_OUTPUT)
def transcode(overwrite):
    """
    It transcode media defined in metadata
    :param overwrite: overwrite current files if exists
    """
    # Get stored movies in tmp_db and process it
    # Total size of entries to fetch
    result, result_count = cache.retrieve()

    if result_count == 0:  # If not data to fetch
        raise exception.EmptyCache()

    logger.log.warning(f"Transcoding {result_count} results")
    # Fetch from each row in tmp db the resources
    for current_movie in check(result):
        logger.log.info("\n")
        logger.log.warn(f"Fetching posters for {current_movie.title}")
        output_dir = util.build_dir(current_movie)
        # process video transcoding/images copy
        media.transcode.posters(current_movie.resource.posters, output_dir)
        logger.log.warn(f"Transcoding {current_movie.title}:{current_movie.imdb_code}")
        media.transcode.videos(current_movie.resource.videos, output_dir, overwrite)

    # Close current tmp cache db
    result.close()
