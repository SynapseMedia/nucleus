from __future__ import annotations
import src.sdk.exceptions as exceptions

from ffmpeg.nodes import FilterableStream as FFMPEG  # type: ignore
from PIL.Image import Image as Pillow

from src.core.types import Path, Any, Mapping
from src.sdk.harvest.model import Media
from .types import Engine


class Video(Engine[FFMPEG]):
    """Engine to support low level transcoding using ffmpeg
    ref: https://github.com/kkroening/ffmpeg-python
    """

    _path: Path
    _options: Mapping[str, Any]

    def output(self, path: Path, **kwargs: Any) -> Media[Path]:
        try:
            # We generate the expected path after transcode
            self._library.spec(path, **kwargs).run()  # type: ignore
            return Media(route=path, type=str(self._library))
        except Exception as e:
            # Standard exceptions raised
            raise exceptions.ProcessingException(str(e))


class Image(Engine[Pillow]):
    """Engine to support image processing using Pillow
    ref: https://pillow.readthedocs.io/en/stable/reference/Image.html
    """

    _path: Path
    _options: Mapping[str, Any]

    def output(self, path: Path, **kwargs: Any) -> Media[Path]:
        # We generate the expected path after processing
        try:
            self._library.save(path, **kwargs)
            return Media(route=path, type=str(self._library))
        except Exception as e:
            # Standard exceptions raised
            raise exceptions.ProcessingException(str(e))


__all__ = ("Video", "Image")
