from __future__ import annotations

import src.sdk.exceptions as exceptions

from collections import ChainMap
from PIL.Image import Image as Pillow
from ffmpeg.nodes import FilterableStream as FFMPEG  # type: ignore

from src.core.types import Path, Any
from src.sdk.harvest.model import Media
from .types import Engine


class Video(Engine[FFMPEG]):
    """Engine to support low level transcoding using ffmpeg
    ref: https://github.com/kkroening/ffmpeg-python
    """

    def _build_output_args(self) -> ChainMap[Any, Any]:
        """Join config as output arguments for ffmpeg"""
        mapped_args = [y for _, y in self.compile()]
        return ChainMap(*mapped_args)

    def save(self, path: Path) -> Media[Path]:
        try:
            # We generate the expected path after transcode
            output_args = self._build_output_args()
            self._library.output(path, **output_args).run()  # type: ignore
            return Media(route=path, type=self._name)
        except Exception as e:
            # Standard exceptions raised
            raise exceptions.ProcessingException(str(e))


class Image(Engine[Pillow]):
    """Engine to support image processing using Pillow
    ref: https://pillow.readthedocs.io/en/stable/reference/Image.html
    """

    def save(self, path: Path) -> Media[Path]:
        # We generate the expected path after processing
        try:
            self._library.save(path)
            return Media(route=path, type=self._name)
        except Exception as e:
            # Standard exceptions raised
            raise exceptions.ProcessingException(str(e))

        # TODO implementar la estructuracion de las opciones y el llamado a los metodos correspondientes


__all__ = ("Video", "Image")
