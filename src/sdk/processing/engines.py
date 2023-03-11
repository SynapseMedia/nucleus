from __future__ import annotations

import src.sdk.processing.transform as transform
import src.sdk.processing.transcode as transcode
import src.sdk.exceptions as exceptions

from src.core.types import Path, Any, Mapping, Adaptable
from src.sdk.harvest.model import Media
from .types import Engine


class Video(Engine):
    """Engine to support low level transcoding using ffmpeg
    ref: https://github.com/kkroening/ffmpeg-python
    """

    _type: str
    _path: Path
    _interface: Adaptable
    _options: Mapping[str, Any]

    def __enter__(self):
        """when context enter initialize input"""
        self._interface = transcode.input(self._path, **self._options)
        return self

    def output(self, path: Path, **kwargs: Any) -> Media[Path]:
        try:
            # We generate the expected path after transcode
            self._interface.spec(path, **kwargs).run()  # type: ignore
            return Media(route=path, type=self._type)
        except Exception as e:
            # Standard exceptions raised
            raise exceptions.ProcessingException(str(e))


class Image(Engine):
    """Engine to support image processing using Pillow
    ref: https://pillow.readthedocs.io/en/stable/reference/Image.html
    """

    _type: str
    _path: Path
    _interface: Adaptable
    _options: Mapping[str, Any]

    def __enter__(self):
        """when context enter initialize input"""
        self._interface = transform.input(self._path, **self._options)
        return self

    def output(self, path: Path, **kwargs: Any) -> Media[Path]:
        # We generate the expected path after processing
        try:
            self._interface.save(path, **kwargs)
            return Media(route=path, type=self._type)
        except Exception as e:
            # Standard exceptions raised
            raise exceptions.ProcessingException(str(e))


__all__ = ("Video", "Image")
