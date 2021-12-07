import click

from src.sdk.scheme.validator import check
from src.sdk import cache, media, logger, util
from src.sdk.constants import OVERWRITE_TRANSCODE_OUTPUT


def _transcode(mv, _format, overwrite):
    logger.log.info("\n")
    output_dir = util.build_dir(mv)
    # process video transcoding
    logger.log.warn(f"Transcoding {mv.title}:{mv.imdb_code}")
    for video in mv.resource.videos:
        media.transcode.ingest.videos(video, output_dir, overwrite)


@click.command()
@click.group("transcode")
@click.option("--overwrite", default=OVERWRITE_TRANSCODE_OUTPUT)
@click.pass_context
def transcode(ctx, overwrite):
    """Transcode toolkit"""
    ctx.ensure_object(dict)
    ctx.obj["overwrite"] = overwrite


@transcode.command()
def single():
    pass


@transcode.command()
@click.pass_context
def batch(ctx):
    """
    Transcode media defined in metadata \n
    Note: Please ensure that metadata exists in local temp db before run this command.
    eg. Resolve meta -> Transcode media
    """
    # Get stored movies in tmp_db and process it
    # Total size of entries to fetch
    result, result_count = cache.manager.safe_retrieve()
    logger.log.warning(f"Transcoding {result_count} results")
    # Fetch from each row in tmp db the resources
    for current_movie in check(result):
        _transcode(current_movie, 'hls', ctx.obj['overwrite'])
    # Close current tmp cache db
    result.close()
