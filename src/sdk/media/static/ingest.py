import time

from src.sdk.media import fetch
from src.sdk import logger, util, media
from src.sdk.constants import RECURSIVE_SLEEP_REQUEST, MAX_FAIL_RETRY


def images(image_path: str, output_dir: str, max_retry=MAX_FAIL_RETRY):
    """
    Recursive poster fetching/copying
    :param image_path: input image path
    :param output_dir: dir to store poster
    :param max_retry:
    :return:
    """
    try:
        file_format = util.extract_extension(image_path)
        root_output_dir, _ = util.resolve_root_for(output_dir)
        input_image = fetch.file(
            image_path, f"{output_dir}/images/large.{file_format}"
        )  # try to fetch image if URL
        tuple(
            media.static.image.auto_resize_to_default(
                str(input_image), f"{root_output_dir}/images"
            )
        )

    except Exception as e:
        if max_retry <= 0:
            raise OverflowError("Max retry exceeded")
        max_retry = max_retry - 1
        logger.log.error(f"Retry download assets error: {e}")
        logger.log.warning(f"Wait {RECURSIVE_SLEEP_REQUEST}")
        time.sleep(RECURSIVE_SLEEP_REQUEST)
        return images(image_path, output_dir, max_retry)
