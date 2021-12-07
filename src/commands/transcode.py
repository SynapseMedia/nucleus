import click
from typing import Iterator
from pathlib import Path
from src.sdk.scheme.validator import check
from src.sdk import cache, media, logger, util
from src.sdk.constants import (
    OVERWRITE_TRANSCODE_OUTPUT,
    PROD_PATH,
    DEFAULT_NEW_FILENAME,
)


def _transcode(mv, _format, overwrite):
    """
    Transcode video listed in metadata
    :param mv: MovieScheme
    :param _format:
    :param overwrite: If true then overwrite current files
    :return:
    """
    logger.log.info("\n")
    output_dir = util.build_dir(mv)
    # process video transcoding
    logger.log.warn(f"Transcoding {mv.title}:{mv.imdb_code}")
    for video in mv.resource.videos:
        output_dir = f"{PROD_PATH}/{output_dir}/{video.quality}/"
        output_dir = f"{output_dir}{DEFAULT_NEW_FILENAME}"
        # Avoid overwrite existing output
        # If path already exist or overwrite = False
        if Path(output_dir).exists() and not overwrite:
            logger.log.warning(f"Skipping media already processed: {output_dir}")
            return

        media.transcode.ingest.videos(
            video,  # Input video file path
            output_dir  # Outpur directory
        )


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
