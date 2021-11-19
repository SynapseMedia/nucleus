import click

from src.sdk.scheme.validator import check
from src.sdk import cache, media, logger, util
from src.sdk.constants import OVERWRITE_TRANSCODE_OUTPUT


@click.command()
@click.option("--overwrite", default=OVERWRITE_TRANSCODE_OUTPUT)
def transcode(overwrite):
    """
    Transcode media defined in metadata \n
    Note: Please ensure that metadata exists in local temp db before run this command.
    eg. Resolve meta -> Transcode media
    """
    # Get stored movies in tmp_db and process it
    # Total size of entries to fetch
    result, result_count = cache.safe_retrieve()
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
