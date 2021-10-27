import click

import os
from src.core import logger, cache
import src.core.mongo as mongo
import src.core.exception as exceptions
import src.core.media as media


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
        raise exceptions.EmptyCache()

    logger.log.warning(f"Transcoding {result_count} results")
    # Fetch from each row in tmp db the resources
    for current_movie in result:
        logger.log.info("\n")
        media.transcode.posters(current_movie)  # process images copy
        # process video transcoding
        media.transcode.videos(current_movie, overwrite)

    # Close current tmp cache db
    result.close()
