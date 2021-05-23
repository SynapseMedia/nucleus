import click
from src.core import logger, Log
import src.core.mongo as mongo
import src.core.media as media
import src.core.helper as helper


@click.command()
def fetch():
    """
    Fetch media from source stores in `tmp db` and copy them to `raw`
    :return:
    """

    # Get stored movies data and process it
    result = helper.cache.retrieve_not_processed(mongo.temp_db)
    result_count = result.count()  # Total size of entries to fetch
    logger.info(f"{Log.WARNING}Fetching {result_count} results{Log.ENDC}")

    # Fetch from each row in tmp db the resources
    for current_movie in result:
        try:
            # Fetch resources if needed
            current_dir = helper.util.build_dir(current_movie)
            media.fetch.image_resources(current_movie, current_dir)
            media.fetch.video_resources(current_movie, current_dir)
        except OverflowError:
            continue

    # Close current tmp cache db
    result.close()
