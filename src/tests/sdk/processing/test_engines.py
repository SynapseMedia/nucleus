import src.sdk.processing as processing

from mock import patch
from src.core.types import Path, Any, List
from src.sdk.harvest import Video, Image, Stream
from src.sdk.harvest.model import Media
from src.sdk.processing.transcode import Screen


class MockImage:
    called: List[str] = []

    def __init__(self):
        self.called = []

    def crop(self, *args: Any, **kwargs: Any):
        self.called.append("crop")
        return self

    def save(*args):
        ...


class MockVideo:
    called: List[str] = []
    kwargs: Any

    def __init__(self):
        self.called = []

    def output(self, path: Path, **kwargs: Any):
        self.kwargs = kwargs
        return self

    def drawbox(self, *args: Any, **kwargs: Any):
        self.called.append("drawbox")
        return self

    def run(self):
        ...


class MockStream(MockVideo):
    def output(self, path: Path, **kwargs: Any):
        preset = processing.transcode.protocol(path.extension())
        self.kwargs = {**preset, **kwargs}
        return self


def test_dispatch_engine(mock_local_video_path: Path):
    """Should dispatch the right engine based on media"""
    stream = Stream(route=mock_local_video_path)
    video = Video(route=mock_local_video_path)
    image = Image(route=mock_local_video_path)

    stream_engine = processing.engine(stream)
    video_engine = processing.engine(video)
    image_engine = processing.engine(image)

    assert isinstance(stream_engine, processing.Stream)
    assert isinstance(video_engine, processing.Video)
    assert isinstance(image_engine, processing.Image)


def test_stream_engine(mock_local_video_path: Path):
    """Should start a valid transcoding process using StreamEngine returning a valid output"""
    with patch("src.sdk.processing.engines.transcode") as mock:

        def _mock_input(_: Any, **y: Any):
            return MockStream()

        mock.input = _mock_input
        media = Stream(route=mock_local_video_path)
        with processing.Stream(media)(
            **{"r": 25, "s": Screen.Q480, "b:v": 1100}
        ) as stream:
            output = Path("video.m3u8")
            media = stream.output(output)

            # Validate output
            assert isinstance(media, Media)
            assert media.route == output


def test_stream_options(mock_local_video_path: Path):
    """Should start a valid transcoding stream process using param options"""
    with patch("src.sdk.processing.engines.transcode") as mock:

        def _mock_input(_: Any, **y: Any):
            return MockStream()

        mock.input = _mock_input
        media = Stream(route=mock_local_video_path)

        input_args = {
            "y": "",
            "c:a": "aac",
            "crf": 0,
            "b:a": "128k",
            "preset": "slow",
            "keyint_min": 100,
            "g": 100,
            "sc_threshold": 0,
        }

        output_args = {"r": 25, "s": Screen.Q480, "b:v": 1100}
        hls_args = {
            "c:v": "libx265",
            "f": "hls",
            "x265-params": "lossless=1",
            "hls_time": 10,
            "hls_list_size": 0,
            "hls_playlist_type": "vod",
            "tag:v": "hvc1",
            **output_args,
        }

        with processing.Stream(media) as video:
            output = Path("video.m3u8")
            video.output(output, **output_args)
            # Check if input receive the right config params
            assert video._options == input_args  # type: ignore
            assert video._input.kwargs == hls_args  # type: ignore


def test_video_engine(mock_local_video_path: Path):
    """Should start a valid transcoding process using VideoEngine returning a valid output"""
    with patch("src.sdk.processing.engines.transcode") as mock:

        def _mock_input(_: Any, **y: Any):
            return MockVideo()

        mock.input = _mock_input
        media = Video(route=mock_local_video_path)
        with processing.Video(media)(**{"t": 20}) as video:
            output = Path("video.mp4")
            media = video.output(output)

            # Validate output
            assert isinstance(media, Media)
            assert media.route == output


def test_video_engine_annotations(mock_local_video_path: Path):
    """Should start a valid transcoding process using method annotations"""
    with patch("src.sdk.processing.engines.transcode") as mock:

        def _mock_input(_: Any, **y: Any):
            return MockVideo()

        mock.input = _mock_input
        media = Video(route=mock_local_video_path)
        with processing.Video(media)(**{"t": 20}) as video:
            output = Path("video.mp4")
            video = video.annotate(
                "drawbox", 50, 50, 120, 120, color="red", thickness=5
            )

            video.output(output)

            assert video._input.called == ["drawbox"]  # type: ignore


def test_video_engine_options(mock_local_video_path: Path):
    """Should start a valid transcoding process using param options"""
    with patch("src.sdk.processing.engines.transcode") as mock:

        def _mock_input(_: Any, **y: Any):
            return MockVideo()

        mock.input = _mock_input
        media = Video(route=mock_local_video_path)
        with processing.Video(media)(**{"t": 20}) as video:
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
        engine = processing.Image(media)

        with engine(a="a") as image:
            output = Path("image.jpg")
            image = image.annotate("crop", (20, 20, 40, 40))
            media = image.output(output)

            # Validate output
            assert isinstance(media, Media)
            assert media.route == output


def test_image_engine_annotations(mock_local_file_path: Path):
    """Should start a valid transform process using using method annotations"""
    with patch("src.sdk.processing.engines.transform") as mock:

        def _mock_input(*_: Any, **a: Any):
            return MockImage()

        mock.input = _mock_input
        media = Image(route=mock_local_file_path)
        engine = processing.Image(media)

        with engine(a="a") as image:
            output = Path("image.jpg")
            image = image.annotate("crop", (20, 20, 40, 40))
            image.output(output)

            assert image._input.called == ["crop"]  # type: ignore


def test_image_engine_options(mock_local_file_path: Path):
    """Should start a valid transform process using  param options"""
    with patch("src.sdk.processing.engines.transform") as mock:

        def _mock_input(*_: Any, **a: Any):
            return MockImage()

        mock.input = _mock_input
        media = Image(route=mock_local_file_path)
        engine = processing.Image(media)

        with engine(a="a") as image:
            output = Path("image.jpg")
            image.output(output)

            # Check if input receive the right config params
            assert image._options == {"a": "a"}  # type: ignore
