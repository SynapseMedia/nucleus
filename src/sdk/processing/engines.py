from src.core.types import Path, Any

from .resize import input as image_input, Input as ImageInput
from .stream import input as stream_input, Input as StreamInput
from .transcode import input as video_input, Input as VideoInput

from .types import Engine


class StreamEngine(Engine):
    """Streaming engine to support video streaming transcoding"""

    _path: Path
    _input: StreamInput
    _options: Any

    def __init__(self, path: Path):
        self.path = path

    def __enter__(self):
        self._input = stream_input(self._path, **self._options)

    def __call__(self, **options: Any):
        self._options = options

    def __getattr__(self, name: str) -> Any:
        return getattr(self._input, name)

    def __exit__(self, *args: Any):
        self._input.terminate()


class VideoEngine(Engine):
    """Video engine to support low level transcoding using ffmpeg"""

    _path: Path
    _input: VideoInput
    _options: Any

    def __init__(self, path: Path):
        self.path = path

    def __enter__(self):
        self._input = video_input(self._path, **self._options)

    def __call__(self, **options: Any):
        self._options = options

    def __getattr__(self, name: str) -> Any:
        """We could interact directly with ffmpeg methods
        ref: https://github.com/kkroening/ffmpeg-python
        """
        return getattr(self._input, name)

    def __exit__(self, *args: Any):
        ...


class ImageEngine(Engine):
    """Image engine to support image processing using Pillow"""

    _path: Path
    _input: ImageInput
    _options: Any

    def __init__(self, path: Path):
        self.path = path

    def __enter__(self):
        self._input = image_input(self._path, **self._options)

    def __call__(self, **options: Any):
        self._options = options

    def __getattr__(self, name: str) -> Any:
        """We could interact directly with Pillow methods
        ref: https://pillow.readthedocs.io/en/stable/reference/Image.html
        """
        return getattr(self._input, name)

    def __exit__(self, *args: Any):
        self._input.close()
