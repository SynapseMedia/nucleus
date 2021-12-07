import click
from src.sdk.scheme.validator import check
from src.sdk import cache, media, logger, util
from src.sdk.constants import (
    OVERWRITE_TRANSCODE_OUTPUT,
)


@click.command()
@click.group("static")
@click.option("--overwrite", default=OVERWRITE_TRANSCODE_OUTPUT)
@click.pass_context
def static(ctx):
    """Statics toolkit"""
    ctx.ensure_object(dict)


@static.group("images")
@click.pass_context
def image():
    """Image toolkit"""
    pass


@image.group("ingest")
@click.pass_context
def ingest():
    pass


@ingest.command()
@click.pass_context
def cached(ctx):
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
        output_dir = util.build_dir(current_movie)
        logger.log.warn(f"Fetching posters for {current_movie.title}")
        logger.log.info("\n")

        # Process each video described in movie
        for _image in current_movie.resource.images:
            media.static.ingest.image(_image, output_dir)

    # Close current tmp cache db
    result.close()
