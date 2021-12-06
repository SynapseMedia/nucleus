import time

import contextlib
import gevent
import os
import shutil
import socket
import tempfile

from ffmpeg_streaming import Formats, Bitrate, Representation, Size
from tqdm import tqdm
from .. import logger, util
from pathlib import Path
from . import fetch
from typing import Iterator
from ..scheme.definition.movies import VideoScheme, PostersScheme
from ..constants import (
    RECURSIVE_SLEEP_REQUEST,
    PROD_PATH,
    DEFAULT_NEW_FILENAME,
    DEFAULT_FORMAT,
    DEFAULT_HLS_TIME,
    MAX_FAIL_RETRY,
)



@contextlib.contextmanager
def progress():
    """Render tqdm progress bar."""
    with tqdm(total=100) as bar:

        def handler(ffmpeg, duration, time_, time_left, process):
                per = round(time_ / duration * 100)
                bar.update(per)

        yield handler


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
            resource_origin = _poster.route  # Input dir resource
            file_format = util.extract_extension(resource_origin)
            fetch.file(resource_origin, f"{output_dir}/{key}.{file_format}")

    except Exception as e:
        if max_retry <= 0:
            raise OverflowError("Max retry exceeded")
        max_retry = max_retry - 1
        logger.log.error(f"Retry download assets error: {e}")
        logger.log.warning(f"Wait {RECURSIVE_SLEEP_REQUEST}")
        time.sleep(RECURSIVE_SLEEP_REQUEST)
        return posters(poster, output_dir, max_retry)


def videos(video_list: Iterator[VideoScheme], output_dir_: str, overwrite):
    """
    Transcode video listed in metadata
    :param video_list: VideoScheme
    :param output_dir_: dir to store video
    :param overwrite: If true then overwrite current files
    :return:
    """

    for video in video_list:
        output_dir = f"{PROD_PATH}/{output_dir_}/{video.quality}/"
        output_dir = f"{output_dir}{DEFAULT_NEW_FILENAME}"

        # Avoid overwrite existing output
        # If path already exist or overwrite = False
        if Path(output_dir).exists() and not overwrite:
            logger.log.warning(f"Skipping media already processed: {output_dir}")
            continue

        util.make_destination_dir(output_dir)
        to_dash(video.route, video.quality,  output_dir)
        logger.log.success(f"New movie stored in: {output_dir}")


def get_representations(quality):
    _144p  = Representation(Size(256, 144), Bitrate(95 * 1024, 64 * 1024))
    _240p  = Representation(Size(426, 240), Bitrate(150 * 1024, 94 * 1024))
    _360p  = Representation(Size(640, 360), Bitrate(276 * 1024, 128 * 1024))
    _480p  = Representation(Size(854, 480), Bitrate(750 * 1024, 192 * 1024))
    _720p  = Representation(Size(1280, 720), Bitrate(2048 * 1024, 320 * 1024))
    _1080p = Representation(Size(1920, 1080), Bitrate(4096 * 1024, 320 * 1024))
    _2k    = Representation(Size(2560, 1440), Bitrate(6144 * 1024, 320 * 1024))
    _4k    = Representation(Size(3840, 2160), Bitrate(17408 * 1024, 320 * 1024))

    return {
        '720p':      [_144p, _240p ,_360p, _480p, _720p],
        '1080p':     [_144p, _240p ,_360p, _480p, _720p, _1080p],
        '2k':        [_144p, _240p ,_360p, _480p, _720p, _1080p, _2k],
        '4k':        [_144p, _240p ,_360p, _480p, _720p, _1080p, _2k, _4k]
    }.get(quality.lower())





def to_dash(input_file, quality, output_dir):
    """
    Transcode movie file to dash
    :param input_file:
    :param output_dir
    :return: new file format dir
    """
    with progress() as progress_handler:
        dash = video.dash(Formats.h264())
        dash.representations(*get_representations(quality))
        dash.output(output_dir, monitor=progress_handler)

    return output_dir
