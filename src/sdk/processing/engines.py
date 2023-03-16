from __future__ import annotations

import re
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

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        # lets compile the pattern to avoid overhead in loop
        self._pattern = re.compile(r"(?<!^)(?=[A-Z])")

    def _to_snake_case(self, class_name: str) -> str:
        """Transform PascalCase class definition to snake_case method name

        :para name: the class name to parse
        :return: the snake case version for class name
        """
        return self._pattern.sub("_", class_name).lower()

    def _setup_methods(self):
        """Call and chain methods based on configured options"""
        for class_name, params in self.compile():
            # The method to call should be the same as the option name.
            method = self._to_snake_case(class_name)
            func = getattr(self._library, method)
            # pillow image chaining
            # all methods return a new instance of the Image class, holding the resulting image
            # ref: https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image
            self._library = func(**dict(params))

    def save(self, path: Path) -> Media[Path]:
        # We generate the expected path after processing
        try:
            self._setup_methods()
            self._library.save(path)
            return Media(route=path, type=self._name)
        except Exception as e:
            # Standard exceptions raised
            raise exceptions.ProcessingException(str(e))


__all__ = ("Video", "Image")
