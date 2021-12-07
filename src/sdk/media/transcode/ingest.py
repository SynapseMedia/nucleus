import time

from .codecs import to_hls
from .. import fetch
from ... import logger, util
from ...scheme.definition.movies import VideoScheme, PostersScheme
from ...constants import (
    RECURSIVE_SLEEP_REQUEST,
    MAX_FAIL_RETRY,
)


def posters(poster: PostersScheme, output_dir: str, max_retry=MAX_FAIL_RETRY):
    """
    Recursive poster fetching
    :param poster: MovieScheme
    :param output_dir: dir to store poster
    :param max_retry:
    :return:
    """
    try:
        for key, _poster in poster.iterable():
            file_format = util.extract_extension(_poster.route)
            fetch.file(_poster.route, f"{output_dir}/{key}.{file_format}")

    except Exception as e:
        if max_retry <= 0:
            raise OverflowError("Max retry exceeded")
        max_retry = max_retry - 1
        logger.log.error(f"Retry download assets error: {e}")
        logger.log.warning(f"Wait {RECURSIVE_SLEEP_REQUEST}")
        time.sleep(RECURSIVE_SLEEP_REQUEST)
        return posters(poster, output_dir, max_retry)


def videos(video: VideoScheme, output_dir: str):
    """
    Transcode video listed in metadata
    :param video: VideoScheme
    :param output_dir: dir to store video
    :return:
    """

    util.make_destination_dir(output_dir)
    to_hls(video.route, video.quality, output_dir)
    logger.log.success(f"New movie stored in: {output_dir}")
