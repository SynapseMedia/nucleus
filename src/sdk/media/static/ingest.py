import time

from src.sdk.media import fetch
from src.sdk import logger, util
from src.sdk.scheme.definition.movies import MediaScheme
from src.sdk.constants import RECURSIVE_SLEEP_REQUEST, MAX_FAIL_RETRY


def images(image: MediaScheme, output_dir: str, max_retry=MAX_FAIL_RETRY):
    """
    Recursive poster fetching/copying
    :param image: MediaScheme
    :param output_dir: dir to store poster
    :param max_retry:
    :return:
    """
    try:
        for key, _poster in image.iterable():
            file_format = util.extract_extension(_poster.route)
            fetch.file(_poster.route, f"{output_dir}/{key}.{file_format}")

    except Exception as e:
        if max_retry <= 0:
            raise OverflowError("Max retry exceeded")
        max_retry = max_retry - 1
        logger.log.error(f"Retry download assets error: {e}")
        logger.log.warning(f"Wait {RECURSIVE_SLEEP_REQUEST}")
        time.sleep(RECURSIVE_SLEEP_REQUEST)
        return images(image, output_dir, max_retry)
