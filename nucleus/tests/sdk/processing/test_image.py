import nucleus.sdk.processing as processing
from nucleus.core.types import Path
from nucleus.sdk.harvest import Image
from nucleus.sdk.processing import Coord, Crop, Resampling, Resize


def test_image_configuration(mock_local_image_path: Path):
    """Should compile the expected configuration"""
    image = Image(path=mock_local_image_path)
    image_engine = processing.engine(image)
    image_engine.configure(Resize(50, 50))
    image_engine.configure(Crop(Coord(0, 0, 50, 50)))

    # check if compiled args are equal to expected
    compiled = sorted(image_engine.compile(), key=lambda t: t[0])
    assert compiled == [
        ('Crop', {'box': (0, 0, 50, 50)}),
        (
            'Resize',
            {'size': (50, 50), 'resample': Resampling.BICUBIC, 'box': (0, 0, 50, 50)},
        ),
    ]
