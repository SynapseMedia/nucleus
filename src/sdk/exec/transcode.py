import shutil
from pathlib import Path
from src.sdk.scheme.definition.movies import MovieScheme
from src.sdk import media, logger, util
from src.sdk.constants import (
    HLS_FORMAT,
    DEFAULT_NEW_FILENAME,
    HLS_NEW_FILENAME,
)


def _run_task(video, output_dir, protocol=HLS_FORMAT, overwrite=True):
    """
    Run transcode task
    :param video: MediaScheme
    :param output_dir: dir to store transcoding video
    :param protocol: Choose live streaming protocol
    :param overwrite: If true then overwrite current files
    :return:
    """

    # process video transcoding
    root_output_dir, _ = util.resolve_root_for(output_dir)
    video_output_dir = f"{root_output_dir}/movie/{protocol}/"
    file_output_dir = f"{video_output_dir}{HLS_NEW_FILENAME if protocol == HLS_FORMAT else DEFAULT_NEW_FILENAME}"

    # Avoid overwrite existing output
    # If path already exist or overwrite = False
    if Path(file_output_dir).exists() and not overwrite:
        logger.log.warning(
            f"Skipping media already processed: {file_output_dir}\n")
        return

    try:
        # Transcode input movie to specified protocol. Default: hls
        media.transcode.ingest.videos(
            video.route,  # Video path
            protocol,  # hls vs dash
            file_output_dir,  # where to store transcoded video
        )
    except RuntimeError:
        shutil.rmtree(
            root_output_dir,
            ignore_errors=True)  # Remove dir if fail
        logger.log.error(f"Fail transcoding to {protocol}")
    return file_output_dir


def boot(current_movie: MovieScheme, **kwargs):
    """
    Boot movie transcode task from metadata definition scheme
    :param current_movie: MovieScheme
    """
    # Process video detailed in movie metadata
    output_dir = util.build_dir(current_movie)
    logger.log.warn(
        f"Transcoding {current_movie.title}:{current_movie.imdb_code}")
    return _run_task(
        video=current_movie.resource.video, output_dir=output_dir, **kwargs
    )
