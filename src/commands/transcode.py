import click
from src.sdk.scheme.validator import check
from src.sdk import cache, logger
from src.sdk.exec import transcode as transcoder
from src.sdk.constants import (
    OVERWRITE_TRANSCODE_OUTPUT,
    HLS_FORMAT,
    DASH_FORMAT
)


@click.group("transcode")
@click.option("--overwrite", default=OVERWRITE_TRANSCODE_OUTPUT)
@click.option(
    "--protocol", default=HLS_FORMAT, type=click.Choice([HLS_FORMAT, DASH_FORMAT])
)
@click.pass_context
def transcode(ctx, overwrite, protocol):
    """Transcode toolkit"""
    ctx.ensure_object(dict)
    ctx.obj["overwrite"] = overwrite
    ctx.obj["protocol"] = protocol


@transcode.command()
@click.pass_context
def single():
    """Transcode arbitrary cid"""
    pass


@transcode.command()
@click.pass_context
def cached(ctx):
    """
    Transcode media defined in cached metadata \n
    Note: Please ensure that metadata exists in local temp db before run this command.
    eg. Resolve meta -> Transcode
    """
    # Get stored movies in tmp_db and process it
    # Total size of entries to fetch
    result, result_count = cache.manager.safe_retrieve()
    logger.log.warning(f"Transcoding {result_count} results")

    # Fetch from each row in tmp db the resources
    # Process video detailed in movie metadata
    for current_movie in check(result):
        transcoder.boot(current_movie, **ctx.obj)

    # Close current tmp cache db
    result.close()
