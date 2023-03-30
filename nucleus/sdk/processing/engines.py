from __future__ import annotations

import re

from collections import ChainMap
from PIL.Image import Image as Pillow
from ffmpeg.nodes import FilterableStream as FFMPEG  # type: ignore

from nucleus.core.types import Path, Any
from nucleus.sdk.exceptions import ProcessingEngineError
from nucleus.sdk.harvest import File
from .types import Engine


class VideoEngine(Engine[FFMPEG]):
    """Engine to support low level transcoding using ffmpeg
    ref: https://github.com/kkroening/ffmpeg-python
    """

    def _build_output_args(self) -> ChainMap[Any, Any]:
        """Join config as output arguments for ffmpeg"""
        mapped_args = [y for _, y in self.compile()]
        return ChainMap(*mapped_args)

    def save(self, path: Path) -> File:
        # TODO allow see ffmpeg progress
        # TODO pubsub? Observer: Keep reading on event?
        try:
            # We generate the expected path after transcode
            output_args = self._build_output_args()
            self._library.output(path, **output_args).run()  # type: ignore
            return File(route=path, type=self._name)
        except Exception as e:
            # Standard exceptions raised
            raise ProcessingEngineError(
                f"error while trying to save video output: {str(e)}"
            )


class ImageEngine(Engine[Pillow]):
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
            # pillow chaining features
            # all methods return a new instance of the Image class, holding the resulting image
            # ref:
            # https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image
            self._library = func(**dict(params))

    def save(self, path: Path) -> File:
        # We generate the expected path after processing
        try:
            self._setup_methods()
            self._library.save(path)
            return File(route=path, type=self._name)
        except Exception as e:
            # Standard exceptions raised
            raise ProcessingEngineError(
                f"error while trying to save image output: {str(e)}"
            )


__all__ = ("VideoEngine", "ImageEngine")
