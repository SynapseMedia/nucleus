import click, os
import shutil
from src.core import logger
import src.core.mongo as mongo
import src.core.helper as helper
import src.core.exception as exceptions
import src.core.media as media
from pathlib import Path

RAW_PATH = media.process.RAW_PATH
PROD_PATH = media.process.PROD_PATH


def _process_images(current_movie):
    current_dir = helper.util.build_dir(current_movie)
    imdb_code = current_movie.get('imdb_code')
    poster_resources = current_movie.get('resource')
    poster_collection = poster_resources.get('posters')

    for k, poster in poster_collection.items():
        poster_path = poster.get('route')
        poster_index = poster.get('index', os.path.basename(poster_path))
        source_path = f"{RAW_PATH}/{current_dir}/{poster_index}"
        path = Path(source_path)

        if not path.is_file():  # If not valid path input
            logger.warning(f"Omit invalid poster file path: {source_path}")
            continue

        destination_path = f"{PROD_PATH}/{imdb_code}/{poster_index}"
        media.process.make_destination_dir(destination_path)
        shutil.copy(source_path, destination_path)
        logger.success(f"Poster copied to {destination_path}")


def _process_videos(current_movie):
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
        path = Path(video_path)

        if not path.is_file():  # If not valid path input
            logger.warning(f"Omit invalid video file path: {video_path}")
            continue

        # Start transcoding process
        logger.info(f"Transcoding {movie_title}:{imdb_code}:{video_quality}")
        logger.info(f"\n")
        output_dir = f"{PROD_PATH}/{imdb_code}/{video_quality}/"
        media.process.make_destination_dir(output_dir)
        media.transcode.to_hls(video_path, output_dir)
        logger.success(f"Movie transcode done for: {output_dir}")


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
        movie_title = current_movie.get('title')
        logger.info(f"Copying posters for {movie_title}")
        _process_images(current_movie)  # process images copy
        logger.info(f"Transcoding videos for {movie_title}")
        _process_videos(current_movie)  # process video transcoding

    # Close current tmp cache db
    result.close()
