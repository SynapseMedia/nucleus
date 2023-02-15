import pytest
import src.core.exceptions as exceptions
import src.sdk.processing.resize as resize

from src.core.types import Path
from src.sdk.processing.resize.types import Sizes


root_dir = "src/tests/_mock/files/"
image_dir_771 = Path(f"{root_dir}771x900.jpg")
image_dir_255 = Path(f"{root_dir}255x255.jpg")
image_dir_638 = Path(f"{root_dir}638x400.jpg")


def test_sizes():
    """Should contains valid image sizes"""

    assert Sizes.Small == (45, 67)
    assert Sizes.Medium == (230, 345)
    assert Sizes.Large == (500, 750)


def test_valid_input():
    """Should success for valid input image"""
    with resize.input(image_dir_771) as img:
        w, h = img.size
        assert w == 771
        assert h == 900


def test_invalid_255x255_input():
    """Should fail image input 255x255 since is less than master 500x750 size"""

    with pytest.raises(exceptions.InvalidImageSize):
        with resize.input(image_dir_255):
            ...


def test_invalid_638x400_input():
    """Should fail if image width is larger than height input 638x400 size"""

    with pytest.raises(exceptions.InvalidImageSize):
        with resize.input(image_dir_638):
            ...
