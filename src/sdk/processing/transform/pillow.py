import PIL.Image as PIL

from src.core.types import Path, Any, Adaptable


class Image(Adaptable):

    _path: Path
    _interface: PIL.Image

    def __init__(self, path: Path, **kwargs: Any):
        self._path = path  # the context file path
        self._interface = PIL.open(path, **kwargs)  # type: ignore

    def __instancecheck__(self, instance: Any):
        return isinstance(instance, self._interface.__class__)

    def __chaining__(self, interface: PIL.Image):
        self._interface = interface

    def __getattr__(self, name: str):
        """Delegate calls to underlying lib.
        ref: https://pillow.readthedocs.io/en/stable/reference/Image.html
        """
        return getattr(self._interface, name)
