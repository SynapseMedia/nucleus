from __future__ import annotations

import re
import inspect
import mimetypes
import PIL.Image
import nucleus.sdk.processing as processing

from collections import ChainMap
from PIL.Image import Image as Pillow
from ffmpeg.nodes import FilterableStream as FFMPEG  # type: ignore

from nucleus.core.types import Path, Any, no_type_check, Dynamic
from nucleus.sdk.exceptions import ProcessingEngineError
from .types import Engine, File, Introspection


@no_type_check
def _to_object(data: Any) -> Any:
    """Recursively convert a nested JSON as Dynamic object

    :return: Dynamic object mirroring JSON representation
    :rtype: Dynamic
    """

    # if is a list recursive parse the entries
    if isinstance(data, list):
        return list(map(_to_object, data))  # type: ignore

    # if is a dict recursive parse
    if isinstance(data, dict):
        container = Dynamic()
        for k, v in data.items():  # type: ignore
            setattr(container, k, _to_object(v))  # type: ignore
        return container

    return data


class VideoEngine(Engine[FFMPEG]):
    """Engine to support low level transcoding using ffmpeg
    ref: https://github.com/kkroening/ffmpeg-python
    """

    def _build_output_args(self) -> ChainMap[Any, Any]:
        """Join config as output arguments for ffmpeg"""
        mapped_args = [y for _, y in self.compile()]
        return ChainMap(*mapped_args)

    def introspect(self, path: Path) -> Introspection:
        # process the arg path or use the current media file path
        (mime_type, _) = mimetypes.guess_type(path)
        probe_result = _to_object(processing.probe(path))

        # extend introspection with custom video ffprobe
        return Introspection(
            size=path.size(),
            type=str(mime_type),
            **vars(probe_result),
        )

    def save(self, path: Path) -> File:
        # TODO allow see ffmpeg progress
        # TODO pubsub? Observer: Keep reading on event?
        try:
            output_args = self._build_output_args()
            # We generate the expected path after transcode
            self._library.output(path, **output_args).run()  # type: ignore

            # after low level processing happen!!
            i8t = self.introspect(path)
            return File(path=path, meta=i8t)
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

    def introspect(self, path: Path) -> Introspection:
        # fet the mime type from file path
        (mime_type, _) = mimetypes.guess_type(path)
        # get attributes from PIL.Image object
        members = inspect.getmembers(PIL.Image.open(path))
        filter_private = filter(lambda x: not x[0].startswith("_"), members)
        filter_method = filter(
            lambda x: not inspect.ismethod(
                x[1]), filter_private)
        image_result = _to_object(dict(filter_method))
        # patch to avoid size conflict keyword
        delattr(image_result, "size")

        # extend introspection with custom PIL.Image attributes
        return Introspection(
            size=path.size(),
            type=str(mime_type),
            **vars(image_result),
        )

    def save(self, path: Path) -> File:
        # We generate the expected path after processing
        try:
            self._setup_methods()
            self._library.save(path)

            # after low level processing happen!!
            i8t = self.introspect(path)
            return File(path=path, meta=i8t)
        except Exception as e:
            # Standard exceptions raised
            raise ProcessingEngineError(
                f"error while trying to save image output: {str(e)}"
            )


__all__ = ("VideoEngine", "ImageEngine")
