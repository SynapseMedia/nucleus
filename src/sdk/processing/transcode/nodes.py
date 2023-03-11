from __future__ import annotations

import ffmpeg  # type: ignore
import functools
import inspect

from src.core.types import Path, Any, Set, Adaptable
from .types import FFMPEG, Spec, Settings


class _Node(Adaptable):
    """Adapter class that amplifies the features of ffmpeg lib.
    We can think about this class as a processing node that uses FFMPEG underneath.
    ref: https://github.com/kkroening/ffmpeg-python
    """

    _path: Path
    _interface: FFMPEG

    def __init__(self, path: Path, **kwargs: Any):
        self._path = path  # the context file path
        self._interface = ffmpeg.input(path, **kwargs)  # type: ignore

    def __instancecheck__(self, instance: Any):
        return isinstance(instance, self._interface.__class__)

    def __chaining__(self, interface: FFMPEG):
        self._interface = interface

    def spec(self, *args: Any, **kwargs: Any) -> Spec:
        """Return current output as stream spec.

        :param path: the path to the output
        :return: output node as stream spec
        :rtype: SpecStream
        """
        return self._interface.output(*args, **kwargs)  # type: ignore

    def probe(self, **kwargs: Any):
        """Delegate call to underlying lib with context input path"""
        return ffmpeg.probe(self._path, **kwargs)  # type: ignore

    def __getattr__(self, name: str):
        """Try proxy calls to underlying lib first.
        If any callable is found in lib return partial function else bound method from input.
        ref: https://kkroening.github.io/ffmpeg-python/
        """

        if hasattr(ffmpeg, name):
            callable_ = getattr(ffmpeg, name)
            args = inspect.getargspec(callable_)

            # we use the default argument if expected `stream` as first param
            # ref: https://kkroening.github.io/ffmpeg-python/
            if "stream" in args.args:
                return functools.partial(callable_, self._interface)

            return callable_
        return getattr(self._interface, name)


# TODO support map to handle multiple streams
# TODO eg: .map(stream, {"s": "840x600", "maxrate": "2M"})


class Video(_Node):
    """Video processing node class implements methods to handle ffmpeg options at a low level."""

    _settings: Set[Settings]

    def aggregate(self, setting: Settings):
        self._settings.add(setting)

    # TODO agregar el manejo de lo settings aca
    # TODO comprobar aca si el formato existe en el origen?
    # TODO para HLS y DASH verificar primero el codec que tiene el original si no es diferente al de salida solo copiar
    # TODO luego convertir cada elemento y unirlo en un solo diccionario y pasarlo al spec.
