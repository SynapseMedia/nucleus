import src.sdk.processing as processing

from mock import patch
from src.core.types import Path, Any, List
from src.sdk.harvest import Video, Image
from src.sdk.harvest.model import Media


class MockImage:
    called: List[str] = []
    chained: List[Any]

    def __init__(self):
        self.called = []
        self.chained = []

    def __instancecheck__(self, instance: Any):
        return True

    def __call__(self, instance: Any):
        self.chained.append(instance)

    def crop(self, *args: Any, **kwargs: Any):
        self.called.append("crop")
        return self

    def save(*args):
        ...


class MockOutput:
    def run(self):
        ...


class MockVideo:
    called: List[str] = []
    output_kwargs: Any
    chained: List[Any]

    def __init__(self):
        self.called = []
        self.chained = []
        self.output_kwargs = {}

    def spec(self, path: Path, **kwargs: Any):
        self.output_kwargs = kwargs
        return self.output(path, **kwargs)

    def output(self, path: Path, **kwargs: Any):
        return MockOutput()

    def __instancecheck__(self, instance: Any):
        return True

    def __call__(self, instance: Any):
        self.chained.append(instance)

    def drawbox(self, *args: Any, **kwargs: Any):
        self.called.append("drawbox")
        return self

    def run(self):
        ...


def test_dispatch_engine(mock_local_video_path: Path, mock_local_image_path: Path):
    """Should dispatch the right engine based on media"""
    video = Video(route=mock_local_video_path)
    image = Image(route=mock_local_image_path)

    video_engine = processing.engine(video)
    image_engine = processing.engine(image)

    assert isinstance(video_engine, processing.Video)
    assert isinstance(image_engine, processing.Image)


def test_video_engine(mock_local_video_path: Path):
    """Should start a valid transcoding process using VideoEngine returning a valid output"""
    with patch("src.sdk.processing.process.FFMPEGAdapter") as mock:

        mock.return_value = MockVideo()
        media = Video(route=mock_local_video_path)

        # Video processing using call to pass input args
        output = Path("video.mp4")
        video = processing.engine(media)
        media = video.save(output)

        # Validate output
        assert media.route == output
        assert isinstance(media, Media)


def test_image_engine(mock_local_image_path: Path):
    """Should start a valid transform process using ImageEngine returning a valid output"""
    with patch("src.sdk.processing.process.PillowAdapter") as mock:

        mock.return_value = MockImage()
        media = Image(route=mock_local_image_path)

        output = Path("image.jpg")
        # expected pillow adapter
        image = processing.engine(media)
        media = image.save(output)

        # Validate output
        assert media.route == output
        assert isinstance(media, Media)
