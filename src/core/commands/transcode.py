import click
import time
import os
from src.core import logger
from pathlib import Path
import src.core.mongo as mongo
import src.core.helper as helper
import src.core.exception as exceptions
import src.core.media as media

RAW_PATH = media.fetch.RAW_PATH
PROD_PATH = media.fetch.PROD_PATH

MAX_FAIL_RETRY = 3
RECURSIVE_SLEEP_REQUEST = 5
OVERWRITE_TRANSCODE_OUTPUT = os.getenv("OVERWRITE_TRANSCODE_OUTPUT", "False") == "True"


def _fetch_posters(current_movie, max_retry=MAX_FAIL_RETRY):
    """
    Recursive poster fetching
    :param current_movie:
    :param max_retry:
    :return:
    """
    try:
        # Fetch resources if needed
        movie_title = current_movie.get("title")
        logger.warn(f"Fetching posters for {movie_title}")
        poster_resources = current_movie.get("resource")
        poster_collection = poster_resources.get("posters")
        # Build dir based on single or mixed resources
        output_dir = helper.util.build_dir(current_movie)

        for key, resource in poster_collection.items():
            resource_origin = resource["route"]  # Input dir resource
            file_format = helper.util.extract_extension(resource_origin)
            media.fetch.file(resource_origin, f"{output_dir}/{key}.{file_format}")

    except Exception as e:
        if max_retry <= 0:
            raise OverflowError("Max retry exceeded")
        max_retry = max_retry - 1
        logger.error(f"Retry download assets error: {e}")
        logger.warning(f"Wait {RECURSIVE_SLEEP_REQUEST}")
        time.sleep(RECURSIVE_SLEEP_REQUEST)
        return _fetch_posters(current_movie, max_retry)


def _transcode_videos(current_movie, overwrite):
    """
    Transcode video listed in metadata
    :param current_movie:
    :return:
    """
    movie_title = current_movie.get("title")
    imdb_code = current_movie.get("imdb_code")
    video_resources = current_movie.get("resource")
    video_collection = video_resources.get("videos")
    # Build dir based on single or mixed resources
    output_dir_ = helper.util.build_dir(current_movie)

    for video in video_collection:
        video_path = video.get("route")
        video_quality = video.get("quality")
        output_dir = f"{PROD_PATH}/{output_dir_}/{video_quality}/"
        output_dir = f"{output_dir}{media.transcode.DEFAULT_NEW_FILENAME}"

        # Avoid overwrite existing output
        # If path already exist or overwrite = False
        if Path(output_dir).exists() and not overwrite:
            logger.warning(f"Skipping media already processed: {output_dir}")
            continue

        logger.warn(f"Transcoding {movie_title}:{imdb_code}:{video_quality}")
        media.fetch.make_destination_dir(output_dir)
        media.transcode.to_hls(video_path, output_dir)
        logger.success(f"New movie stored in: {output_dir}")


@click.command()
@click.option("--overwrite", default=OVERWRITE_TRANSCODE_OUTPUT)
def transcode(overwrite):
    """
    It transcode media defined in metadata
    """
    # Get stored movies in tmp_db and process it
    result = helper.cache.retrieve(mongo.temp_db)
    result_count = result.count()  # Total size of entries to fetch

    if result_count == 0:  # If not data to fetch
        raise exceptions.EmptyCache()

    logger.warning(f"Transcoding {result_count} results")
    # Fetch from each row in tmp db the resources
    for current_movie in result:
        logger.info(f"\n")
        _fetch_posters(current_movie)  # process images copy
        # process video transcoding
        _transcode_videos(current_movie, overwrite)

    # Close current tmp cache db
    result.close()
