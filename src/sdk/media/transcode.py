import ffmpeg
import time

import contextlib
import gevent
import os
import shutil
import socket
import tempfile

from tqdm import tqdm
from .. import logger, util
from pathlib import Path
from . import fetch

DEFAULT_FORMAT = "hls"
DEFAULT_HLS_TIME = 5
DEFAULT_HLS_FORMAT = "m3u8"
DEFAULT_NEW_FILENAME = "index.m3u8"

MAX_FAIL_RETRY = 3
RECURSIVE_SLEEP_REQUEST = 5
RAW_PATH = os.getenv("RAW_DIRECTORY")
PROD_PATH = os.getenv("PROD_DIRECTORY")


# from
# https://github.com/kkroening/ffmpeg-python/blob/master/examples/show_progress.py
@contextlib.contextmanager
def _tmpdir_scope():
    tmpdir = tempfile.mkdtemp()
    try:
        yield tmpdir
    finally:
        shutil.rmtree(tmpdir)


def _do_watch_progress(_, sock, handler):
    """Function to run in a separate gevent greenlet to read progress
    events from a unix-domain socket."""
    connection, client_address = sock.accept()
    data = b""
    try:
        while True:
            more_data = connection.recv(16)
            if not more_data:
                break
            data += more_data
            lines = data.split(b"\n")
            for line in lines[:-1]:
                line = line.decode()
                parts = line.split("=")
                key = parts[0] if len(parts) > 0 else None
                value = parts[1] if len(parts) > 1 else None
                handler(key, value)
            data = lines[-1]
    finally:
        connection.close()


@contextlib.contextmanager
def _watch_progress(handler):
    """Context manager for creating a unix-domain socket and listen for
    ffmpeg progress events.
    The socket filename is yielded from the context manager and the
    socket is closed when the context manager is exited.
    Args:
        handler: a function to be called when progress events are
            received; receives a ``key`` argument and ``value``
            argument. (The example ``show_progress`` below uses tqdm)
    Yields:
        socket_filename: the name of the socket file.
    """
    with _tmpdir_scope() as tmpdir:
        socket_filename = os.path.join(tmpdir, "sock")
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        with contextlib.closing(sock):
            sock.bind(socket_filename)
            sock.listen(1)
            child = gevent.spawn(_do_watch_progress, socket_filename, sock, handler)
            try:
                yield socket_filename
            except BaseException:
                gevent.kill(child)
                raise


@contextlib.contextmanager
def progress(total_duration):
    gevent.monkey.patch_all()

    """Create a unix-domain socket to watch progress and render tqdm
    progress bar."""
    with tqdm(total=round(total_duration, 2)) as bar:

        def handler(key, value):
            if key == "out_time_ms":
                time = round(float(value) / 1000000.0, 2)
                bar.update(time - bar.n)
            elif key == "progress" and value == "end":
                bar.update(bar.total - bar.n)

        with _watch_progress(handler) as socket_filename:
            yield socket_filename


def posters(current_movie, max_retry=MAX_FAIL_RETRY):
    """
    Recursive poster fetching
    :param current_movie: MovieScheme
    :param max_retry:
    :return:
    """
    try:
        # Fetch resources if needed
        movie_title = current_movie.get("title")
        logger.log.warn(f"Fetching posters for {movie_title}")
        poster_resources = current_movie.get("resource")
        poster_collection = poster_resources.get("posters")
        # Build dir based on single or mixed resources
        output_dir = util.build_dir(current_movie)

        for key, resource in poster_collection.items():
            resource_origin = resource["route"]  # Input dir resource
            file_format = util.extract_extension(resource_origin)
            fetch.file(resource_origin, f"{output_dir}/{key}.{file_format}")

    except Exception as e:
        if max_retry <= 0:
            raise OverflowError("Max retry exceeded")
        max_retry = max_retry - 1
        logger.log.error(f"Retry download assets error: {e}")
        logger.log.warning(f"Wait {RECURSIVE_SLEEP_REQUEST}")
        time.sleep(RECURSIVE_SLEEP_REQUEST)
        return posters(current_movie, max_retry)


def videos(current_movie, overwrite):
    """
    Transcode video listed in metadata
    :param current_movie:
    :param overwrite: If true then overwrite current files
    :return:
    """
    movie_title = current_movie.get("title")
    imdb_code = current_movie.get("imdb_code")
    video_resources = current_movie.get("resource")
    video_collection = video_resources.get("videos")
    # Build dir based on single or mixed resources
    output_dir_ = util.build_dir(current_movie)

    for video in video_collection:
        video_path = video.get("route")
        video_quality = video.get("quality")
        output_dir = f"{PROD_PATH}/{output_dir_}/{video_quality}/"
        output_dir = f"{output_dir}{DEFAULT_NEW_FILENAME}"

        # Avoid overwrite existing output
        # If path already exist or overwrite = False
        if Path(output_dir).exists() and not overwrite:
            logger.log.warning(f"Skipping media already processed: {output_dir}")
            continue

        logger.log.warn(f"Transcoding {movie_title}:{imdb_code}:{video_quality}")
        util.make_destination_dir(output_dir)
        to_hls(video_path, output_dir)
        logger.log.success(f"New movie stored in: {output_dir}")


def to_hls(input_file, output_dir):
    """
    Transcode movie file to hls
    :param input_file:
    :param output_dir
    :return: new file format dir
    """

    probe = ffmpeg.probe(input_file)
    total_duration = float(probe["format"]["duration"])
    video_stream = next(
        (stream for stream in probe["streams"] if stream["codec_type"] == "video"),
        None,
    )

    # When transcoding audio and/or video streams, ffmpeg will not begin writing into the output until it has one
    # packet for each such stream. While waiting for that to happen, packets for other streams are buffered.
    # This option sets the size of this buffer, in packets, for the matching
    # output stream.
    output_args = {"max_muxing_queue_size": 9999}
    if video_stream["codec_name"] == "h264":
        output_args["vcodec"] = "copy"
        logger.log.success("vcodec copy mode: enabled")

    with progress(total_duration) as socket_filename:
        try:
            (
                ffmpeg.input(input_file)
                .output(
                    output_dir,
                    format=DEFAULT_FORMAT,
                    start_number=0,
                    hls_time=DEFAULT_HLS_TIME,
                    hls_list_size=0,
                    **output_args,
                )
                .global_args("-progress", "unix://{}".format(socket_filename))
                .run(
                    overwrite_output=True,
                    capture_stdout=True,
                    capture_stderr=True,
                )
            )
        except ffmpeg.Error as e:
            print(e.stderr)
            logger.log.error(f"Error transcoding {input_file}")

    return output_dir
