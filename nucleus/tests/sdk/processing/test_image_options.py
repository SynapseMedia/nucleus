from nucleus.sdk.processing import Coord, Crop, Resampling, Resize


def test_resize_option():
    """Should return expected Resize as dict"""

    resize = Resize(100, 100)
    resize.crop(Coord(0, 0, 10, 10))
    resize.resample(Resampling.BOX)

    expected_size = {
        'size': (100, 100),
        'resample': Resampling.BOX,
        'box': (0, 0, 10, 10),
    }

    assert dict(resize) == expected_size


def test_crop_option():
    """Should return expected Crop as dict"""

    crop = Crop(Coord(0, 0, 10, 10))
    expected_fps = {'box': (0, 0, 10, 10)}
    assert dict(crop) == expected_fps
