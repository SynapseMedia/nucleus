import click

import os
from src.sdk.scheme.validator import parse
from src.sdk import cache, mongo, media, logger, exception

OVERWRITE_TRANSCODE_OUTPUT = os.getenv("OVERWRITE_TRANSCODE_OUTPUT", "False") == "True"


@click.command()
@click.option("--overwrite", default=OVERWRITE_TRANSCODE_OUTPUT)
def transcode(overwrite):
    """
    It transcode media defined in metadata
    """
    # Get stored movies in tmp_db and process it
    result = cache.retrieve(mongo.temp_db)
    result_count = result.count()  # Total size of entries to fetch

    if result_count == 0:  # If not data to fetch
        raise exception.EmptyCache()

    logger.log.warning(f"Transcoding {result_count} results")
    # Fetch from each row in tmp db the resources
    for current_movie in parse(result):
        logger.log.info("\n")
        # process video transcoding
        # process images copy
        media.transcode.posters(current_movie)
        media.transcode.videos(current_movie, overwrite)

    # Close current tmp cache db
    result.close()
