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

    def __chaining__(self, instance: Any):
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
        return MockOutput()

    def __instancecheck__(self, instance: Any):
        return True

    def __chaining__(self, instance: Any):
        self.chained.append(instance)

    def drawbox(self, *args: Any, **kwargs: Any):
        self.called.append("drawbox")
        return self

    def run(self):
        ...


# TODO test video settings


def test_video_engine(mock_local_video_path: Path):
    """Should start a valid transcoding process using VideoEngine returning a valid output"""
    with patch("src.sdk.processing.engines.transcode") as mock:

        def _mock_input(_: Any, **y: Any):
            return MockVideo()

        mock.input = _mock_input
        media = Video(route=mock_local_video_path)

        # Video processing using call to pass input args
        with processing.Video(media, t=20) as video:
            output = Path("video.mp4")
            media = video.output(output)

            # Validate output
            assert media.route == output
            assert isinstance(media, Media)


def test_video_engine_annotations(mock_local_video_path: Path):
    """Should start a valid transcoding process using method annotations"""
    with patch("src.sdk.processing.engines.transcode") as mock:

        def _mock_input(_: Any, **y: Any):
            return MockVideo()

        mock.input = _mock_input
        media = Video(route=mock_local_video_path)
        with processing.Video(media, t=20) as video:
            output = Path("video.mp4")
            video = video.annotate(
                "drawbox", 50, 50, 120, 120, color="red", thickness=5
            )

            video.output(output)
            assert video._interface.called == ["drawbox"]  # type: ignore
            assert isinstance(video._interface.chained[0], MockVideo)  # type: ignore


def test_video_engine_options(mock_local_video_path: Path):
    """Should start a valid transcoding process using param options"""
    with patch("src.sdk.processing.engines.transcode") as mock:

        def _mock_input(_: Any, **y: Any):
            return MockVideo()

        mock.input = _mock_input
        media = Video(route=mock_local_video_path)
        with processing.Video(media, t=20) as video:
            output = Path("video.mp4")
            video.output(output)

            # Check if input receive the right config params
            assert video._options == {"t": 20}  # type: ignore


def test_image_engine(mock_local_file_path: Path):
    """Should start a valid transform process using ImageEngine returning a valid output"""
    with patch("src.sdk.processing.engines.transform") as mock:

        def _mock_input(*_: Any, **a: Any):
            return MockImage()

        mock.input = _mock_input
        media = Image(route=mock_local_file_path)

        with processing.Image(media) as image:
            output = Path("image.jpg")
            image = image.annotate("crop", (20, 20, 40, 40))
            media = image.output(output)

            # Validate output
            assert media.route == output
            assert isinstance(media, Media)


def test_image_engine_annotations(mock_local_file_path: Path):
    """Should start a valid transform process using using method annotations"""
    with patch("src.sdk.processing.engines.transform") as mock:

        def _mock_input(*_: Any, **a: Any):
            return MockImage()

        mock.input = _mock_input
        media = Image(route=mock_local_file_path)

        with processing.Image(media) as image:
            output = Path("image.jpg")
            image = image.annotate("crop", (20, 20, 40, 40))
            image.output(output)

            assert image._interface.called == ["crop"]  # type: ignore
            assert isinstance(image._interface.chained[0], MockImage)  # type: ignore


def test_image_engine_options(mock_local_file_path: Path):
    """Should start a valid transform process using  param options"""
    with patch("src.sdk.processing.engines.transform") as mock:

        def _mock_input(*_: Any, **a: Any):
            return MockImage()

        mock.input = _mock_input
        media = Image(route=mock_local_file_path)

        with processing.Image(media, mode="r") as image:
            output = Path("image.jpg")
            image.output(output)

            # Check if input receive the right config params
            assert image._options == {"mode": "r"}  # type: ignore
