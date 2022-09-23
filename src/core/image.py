import dataclasses
import contextlib
import PIL.Image as PIL
import src.core.exceptions as exceptions

# Convention for importing types
from src.core.types import Directory, Iterator


@dataclasses.dataclass(frozen=True)
class Size:
    Small = (45, 67)
    Medium = (230, 345)
    Large = (500, 750)


def _invalid(image: PIL.Image) -> bool:
    """Validate ratio for image

    :param image: Image to validate
    :return: True if image is valid, False otherwise
    :rtype: bool
    """
    # input ratio size
    w, h = image.size
    # ratio height should be major than width
    is_height_less_than_width = h < w
    # input image is smaller than "master"
    is_input_less_than_master = any(x < y for x, y in zip(image.size, Size.Large))
    # Invalid image ratio height should be major than width
    return is_height_less_than_width or is_input_less_than_master


@contextlib.contextmanager
def input(input_image: Directory) -> Iterator[PIL.Image]:
    """Factory Image

    :param input_image: Path to image
    :return: PIL Image object
    :rtype: Image
    :raises InvalidImageSize: if the image ratio is invalid
    """

    with PIL.open(input_image) as image:
        if _invalid(image):
            # Invalid image ratio height should be major than width
            raise exceptions.InvalidImageSize()
        yield image
