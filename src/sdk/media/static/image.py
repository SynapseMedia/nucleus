from PIL import Image
from src.sdk import logger, util
from contextlib import contextmanager

SMALL = "small"
MEDIUM = "medium"
LARGE = "large"


class Sizes:
    Small = (67, 45)
    Medium = (345, 230)
    Large = (750, 500)


@contextmanager
def open_image(input_image: str):
    """
    Factory Image function
    :param input_image: Path to image
    :return Image object
    """
    image = Image.open(input_image)
    logger.log.info(f"Image format: {image.format}")
    logger.log.info(f"Image mode: {image.mode}")
    logger.log.info(f"Image size: {image.size}")
    yield image


# TODO write tests
def get_representations(size: str):
    """
    Return representation list based on`size`.
    Blocked upscale and locked downscale allowed for each defined quality
    :param size:
    :return list of representations based on requested size
    """

    return {
        SMALL: Sizes.Small,
        MEDIUM: Sizes.Medium,
        LARGE: Sizes.Large,
    }.get(size.lower())


# TODO write tests
def auto_resize_to_default(input_image: str, output: str):
    """
    Resize image and keep their aspect ratios
    :param input_image: Path to image
    :param output: Where store the resized image
    """

    for size in {SMALL, MEDIUM, LARGE}:
        file_format = util.extract_extension(input_image)
        yield resize_thumbnails(
            input_image, f"{output}/images/{size}.{file_format}", size
        )


# TODO write tests
def resize_thumbnails(input_image: str, output: str, size) -> Image:
    """
    Resize image and keep their aspect ratios
    :param input_image: Path to image
    :param output: Where store the resized image
    :param size: Size to resize
    """

    # Keep original requested size if `size` is Size subtype
    size_representation = (
        get_representations(size) if not isinstance(size, Sizes) else size
    )
    # Avoid pass if invalid representation or not `size` subtype
    if not size_representation and not isinstance(size, Sizes):
        raise ValueError(
            "Invalid size representation. Please provide valid one. eg: small, medium, large"
        )

    with open_image(input_image) as image:
        if not image.size > Sizes.Large:
            # Same size. Just keep original
            return input_image

        logger.log.warn(f"Resizing image {image.size}->{size}")
        image.thumbnail(size)
        image.save(output)
        return image
