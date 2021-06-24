import click
from src.core import logger
import src.core.mongo as mongo
import src.core.helper as helper
import src.core.exception as exceptions
import src.core.media as media
from pathlib import Path


@click.command()
@click.option('--copy-assets', default=True)
def transcode(copy_assets):
    """
    It fetch/store media defined in metadata
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
        video_resources = current_movie.get('resource')
        video_collection = video_resources.get('videos')

        for video in video_collection:
            video_path = video.get('route')
            path = Path(video_path)

            if not path.is_file():  # If not valid path input
                logger.warning(f"Omit invalid file path {video_path}")
                continue

            # Start transcoding process
            media.transcode.to_hls(video_path)

    # Close current tmp cache db
    result.close()
