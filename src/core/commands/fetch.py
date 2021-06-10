import click, time
from src.core import logger
import src.core.mongo as mongo
import src.core.media as media
import src.core.helper as helper
import src.core.exception as exceptions

MAX_FAIL_RETRY = 3
RECURSIVE_SLEEP_REQUEST = 5


def _process_media(current_movie, max_retry):
    """
    Recursive media fetching
    :param current_movie:
    :param max_retry:
    :return:
    """
    try:
        # Fetch resources if needed
        logger.warning(f"Processing: {current_movie.get('imdb_code')}")
        current_dir = helper.util.build_dir(current_movie)
        media.fetch.image_resources(current_movie, current_dir)
        media.fetch.video_resources(current_movie, current_dir)
        logger.info("\n")
    except Exception as e:
        if max_retry <= 0:
            raise OverflowError('Max retry exceeded')
        max_retry = max_retry - 1
        logger.error(f"Retry download assets error: {e}")
        logger.warning(f"Wait {RECURSIVE_SLEEP_REQUEST}")
        time.sleep(RECURSIVE_SLEEP_REQUEST)
        return _process_media(current_movie, max_retry)


@click.command()
@click.option('--max-retry', default=MAX_FAIL_RETRY)
def fetch(max_retry):
    """
    It fetch/store media defined in metadata
    """
    # Get stored movies in tmp_db and process it
    result = helper.cache.retrieve(mongo.temp_db)
    result_count = result.count()  # Total size of entries to fetch

    if result_count == 0:  # If not data to fetch
        raise exceptions.EmptyCache()

    logger.warning(f"Fetching {result_count} results")
    # Fetch from each row in tmp db the resources
    for current_movie in result:
        try:
            _process_media(current_movie, max_retry)
        except OverflowError:
            continue
    # Close current tmp cache db
    result.close()
