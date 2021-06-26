import click
import time
from src.core import logger
import src.core.mongo as mongo
import src.core.helper as helper
import src.core.exception as exceptions
import src.core.media as media

RAW_PATH = media.process.RAW_PATH
PROD_PATH = media.process.PROD_PATH

MAX_FAIL_RETRY = 3
RECURSIVE_SLEEP_REQUEST = 5


def _fetch_posters(current_movie, max_retry=MAX_FAIL_RETRY):
    """
    Recursive poster fetching
    :param current_movie:
    :param max_retry:
    :return:
    """
    try:
        # Fetch resources if needed
        imdb_code = current_movie.get('imdb_code')
        movie_title = current_movie.get('title')
        logger.warn(f"Fetching posters for {movie_title}")
        media.fetch.image_resources(current_movie, imdb_code)
    except Exception as e:
        if max_retry <= 0:
            raise OverflowError('Max retry exceeded')
        max_retry = max_retry - 1
        logger.error(f"Retry download assets error: {e}")
        logger.warning(f"Wait {RECURSIVE_SLEEP_REQUEST}")
        time.sleep(RECURSIVE_SLEEP_REQUEST)
        return _fetch_posters(current_movie, max_retry)


def _transcode_videos(current_movie):
    """
    Transcode video listed in metadata
    :param current_movie:
    :return:
    """
    movie_title = current_movie.get('title')
    imdb_code = current_movie.get('imdb_code')
    video_resources = current_movie.get('resource')
    video_collection = video_resources.get('videos')

    for video in video_collection:
        video_path = video.get('route')
        video_quality = video.get('quality')

        # Start transcoding process
        logger.warn(f"Transcoding {movie_title}:{imdb_code}:{video_quality}")
        output_dir = f"{PROD_PATH}/{imdb_code}/{video_quality}/"
        media.process.make_destination_dir(output_dir)
        media.transcode.to_hls(video_path, output_dir)
        logger.success(f"New movie stored in: {output_dir}")


@click.command()
def transcode():
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
        # transcode video file from mp4
        logger.info(f"\n")
        _fetch_posters(current_movie)  # process images copy
        _transcode_videos(current_movie)  # process video transcoding

    # Close current tmp cache db
    result.close()
