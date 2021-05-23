import click, time
from src.core import logger, Log
import src.core.mongo as mongo
import src.core.media as media
import src.core.helper as helper

RECURSIVE_SLEEP_REQUEST = 10


@click.command()
@click.option('--retry')
def fetch(max_retry):
    """
    Fetch media from source stores in `tmp db` and copy them to `raw`
    :return:
    """

    # Get stored movies in tmp_db and process it
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
        except Exception as e:
            if max_retry <= 0:
                raise OverflowError('Max retry exceeded')
            max_retry = max_retry - 1
            logger.info(e)
            logger.error(f"Retry download assets error: {e}")
            logger.warning(f"{Log.WARNING}Wait {RECURSIVE_SLEEP_REQUEST}{Log.ENDC}")
            time.sleep(RECURSIVE_SLEEP_REQUEST)
            result.close()  # Close current tmp cache db
            return fetch(max_retry)
        except OverflowError:
            continue

    # Close current tmp cache db
    result.close()
