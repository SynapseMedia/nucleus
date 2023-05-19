from __future__ import annotations

import inspect
import mimetypes
import re
from collections import ChainMap

import PIL.Image
from ffmpeg.nodes import FilterableStream as FFMPEG
from PIL.Image import Image as Pillow

import nucleus.sdk.processing as processing
from nucleus.core.types import Any, Dynamic, Path, no_type_check
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
            setattr(container, str(k), _to_object(v))  # type: ignore
        return container

    return data


class VideoEngine(Engine):
    """Engine adapt FFMPEG to support low level transcoding
    ref: https://github.com/kkroening/ffmpeg-python
    """

    def __init__(self, lib: FFMPEG):
        super().__init__(lib)

    def _build_output_args(self) -> ChainMap[Any, Any]:
        """Join config as output arguments for ffmpeg"""
        mapped_args = [y for _, y in self.compile()]
        return ChainMap(*mapped_args)

    def introspect(self, path: Path) -> Introspection:
        # process the arg path or use the current media file path
        (mime_type, _) = mimetypes.guess_type(path)
        video_introspection = _to_object(processing.probe(path))

        # extend introspection with custom video ffprobe
        return Introspection(
            size=path.size(),
            type=str(mime_type),
            **vars(video_introspection),
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
            raise ProcessingEngineError(f'error while trying to save video output: {str(e)}')


class ImageEngine(Engine):
    """Engine adapt Pillow to support image processing
    ref: https://pillow.readthedocs.io/en/stable/reference/Image.html
    """

    def __init__(self, lib: Pillow):
        # compile the pattern to avoid overhead in loop and bind underlying lib
        self._pattern = re.compile(r'(?<!^)(?=[A-Z])')
        super().__init__(lib)

    def _to_snake_case(self, class_name: str) -> str:
        """Transform PascalCase class definition to snake_case method name

        :para name: the class name to parse
        :return: the snake case version for class name
        """
        return self._pattern.sub('_', class_name).lower()

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
        filter_private = filter(lambda x: not x[0].startswith('_'), members)
        filter_method = filter(lambda x: not inspect.ismethod(x[1]), filter_private)
        image_introspection = _to_object(dict(filter_method))
        # patch to avoid size conflict keyword
        delattr(image_introspection, 'size')

        # extend introspection with custom PIL.Image attributes
        return Introspection(
            size=path.size(),
            type=str(mime_type),
            **vars(image_introspection),
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
            raise ProcessingEngineError(f'error while trying to save image output: {str(e)}')


__all__ = ('VideoEngine', 'ImageEngine')
