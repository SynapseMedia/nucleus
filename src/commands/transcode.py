import click
import shutil
from pathlib import Path
from src.sdk.scheme.validator import check
from src.sdk import cache, media, logger, util
from src.sdk.constants import (
    OVERWRITE_TRANSCODE_OUTPUT,
    PROD_PATH,
    HLS_FORMAT,
    DASH_FORMAT,
    DEFAULT_NEW_FILENAME,
    HLS_NEW_FILENAME,
)


def _transcode(video, output_dir, protocol, overwrite):
    """
    Transcode video listed in metadata
    :param video: VideoScheme
    :param output_dir: dir to store transcoding video
    :param protocol: Choose live streaming protocol
    :param overwrite: If true then overwrite current files
    :return:
    """

    # process video transcoding
    root_output_dir = f"{PROD_PATH}/{output_dir}"
    video_output_dir = f"{root_output_dir}/video/"
    file_output_dir = f"{video_output_dir}{HLS_NEW_FILENAME if protocol == HLS_FORMAT else DEFAULT_NEW_FILENAME}"

    # Avoid overwrite existing output
    # If path already exist or overwrite = False
    if Path(file_output_dir).exists() and not overwrite:
        logger.log.warning(f"Skipping media already processed: {file_output_dir}\n")
        return

    try:
        # Transcode input movie to specified protocol. Default: hls
        media.transcode.ingest.videos(video, protocol, file_output_dir)
    except RuntimeError as e:
        print(e)
        shutil.rmtree(root_output_dir, ignore_errors=True) # Remove dir if fail
        logger.log.error(f"Fail transcoding to {protocol}")


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
    for current_movie in check(result):
        # Process video detailed in movie metadata
        output_dir = util.build_dir(current_movie)
        logger.log.warn(f"Transcoding {current_movie.title}:{current_movie.imdb_code}")
        _transcode(video=current_movie.resource.video, output_dir=output_dir, **ctx.obj)

    # Close current tmp cache db
    result.close()
