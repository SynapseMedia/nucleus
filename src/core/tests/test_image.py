import pytest
from src.core.image import input, Size
from src.core.exceptions import InvalidImageSize


def test_sizes():
    """Should contains valid image sizes"""

    assert Size.Small == (45, 67)
    assert Size.Medium == (230, 345)
    assert Size.Large == (500, 750)


def test_valid_input():
    """Should success for valid input image"""
    with input("src/core/tests/data/771x900.jpg") as image:
        w, h = image.size
        assert w == 771
        assert h == 900


def test_invalid_255x255_input():
    """Should fail image input 255x255 since is less than master 500x750 size"""

    with pytest.raises(InvalidImageSize):
        with input("src/core/tests/data/255x255.jpg"):
            ...


def test_invalid_638x400_input():
    """Should fail if image width is larger than height input 638x400 size"""

    with pytest.raises(InvalidImageSize):
        with input("src/core/tests/data/638x400.jpeg"):
            ...
