import sys

import click
from src.sdk.scheme.validator import check
from src.sdk import cache, media, logger, util


@click.group("static")
def static():
    """Statics toolkit"""
    pass


@static.group("images")
def images():
    """Image toolkit"""
    pass


@images.group("ingest")
def ingest():
    pass


@ingest.command()
def cached():
    """
    Convert/Process image static defined in cached metadata \n
    Note: Please ensure that metadata exists in local temp db before run this command.
    eg. Resolve -> Static
    """
    # Get stored movies in tmp_db and process it
    # Total size of entries to fetch
    result, result_count = cache.manager.safe_retrieve()
    logger.log.warning(f"Processing {result_count} results")

    # Fetch from each row in tmp db the resources
    for current_movie in check(result):
        # Process each video described in movie
        output_dir = util.build_dir(current_movie)
        logger.log.warn(f"Fetching posters for {current_movie.title}")
        media.static.ingest.images(
            image_path=current_movie.resource.image.route,  # input image path
            output_dir=output_dir,  # where store new images?
        )
        sys.stdout.write("\n")

    # Close current tmp cache db
    result.close()
