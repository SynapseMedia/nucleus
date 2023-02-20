from src.core.types import Path, Any
from .resize import input as image_input
from .resize.types import ImageInput
from .transcode import HLS, DASH, input as video_input
from .transcode.types import VideoInput
from .types import Engine


class VideoEngine(Engine):

    _path: Path
    _input: VideoInput
    _options: Any

    __protocols__ = ("to_hls", "to_dash")

    def __init__(self, path: Path):
        self.path = path

    def __enter__(self):
        self._input = video_input(self._path, **self._options)

    def __call__(self, **options: Any):
        self._options = options

    def __getattr__(self, name: str) -> Any:
        """We extend methods from ffmpeg lib adding our "out of the box" protocols
        ref: https://github.com/kkroening/ffmpeg-python
        """
        if name not in self.__protocols__:
            return getattr(self._input, name)

        ffinput = self._input.get_media()  # get input media to process
        return dict(zip(self.__protocols__, (HLS(ffinput), DASH(ffinput))))[name]

    def __exit__(self, *args: Any):
        ...


class ImageEngine(Engine):

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
        
