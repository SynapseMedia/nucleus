from __future__ import annotations

from abc import abstractmethod, ABC
from src.core.types import Any, Path, URL, Mapping, Union
from src.sdk.harvest.model import Media

# Alias for allowed engine inputs
Processable = Media[Union[Path, URL]]


class Engine(ABC):
    """Adapter/Template engine to handle standard actions for media processing.

    Any type of input, for example, video, image, music, etc., needs some type of processing to be transmitted or consumed.
    We could define any steps or logic needed to process our media.
    """

    _type: str
    _path: Path
    _input: Any
    _options: Mapping[str, Any]

    def __init__(self, media: Processable):
        """Template method initialize engine with media input path."""
        self._path = Path(media.route)
        self._type = media.type
        self._options = {}  # we could ad any default options here

    def __call__(self, **options: Any) -> Engine:
        """Template method to extend options for processing context.
        IMPORTANT! This methods extend using update strategy so can overwrite existing options.

        :param options: additional input arguments
        :return: Engine instance
        :rtype: Engine
        """
        self._options = {**self._options, **options}
        return self

    def __exit__(self, *args: Any):
        """Template method to handle context exit. Default is do nothing.
        Defines what the context manager should do after its block has been executed (or terminates)"""
        ...

    def __getattr__(self, name: str) -> Any:
        """Delegate calls to any underlying tool or library.

        :param name: the name of the method to call
        :return: any returned result by underlying method
        :rtype: Any
        :raise ValueError if accessed attribute is not callable
        """

        method = getattr(self._input, name)
        if not callable(method):
            raise ValueError("expected call to underlying method")

        # call to method and return
        return method

    def annotate(self, name: str, *args: Any, **kwargs: Any) -> Engine:
        """It allow chain calls for underlying methods keeping object reference.

        :param name: the name of the method to call
        :param kwargs: additional keyword arguments
        :return: annotated engine
        :rtype: Engine
        """

        # concat `fluent interface`
        call = getattr(self, name)
        result = call(name, *args, **kwargs)
        if result is not None:
            self._input = result
        return self

    @abstractmethod
    def __enter__(self) -> Engine:
        """Defines what the context manager should do at the beginning of the block created by the with statement."""
        ...

    @abstractmethod
    def output(self, path: Path, **kwargs: Any) -> Media[Path]:
        """Standard processed media output.
        Expected call output to get resulting File output.

        eg.
            with Engine(Path(...)) as stream:
                ...more code here
                stream.output(Path(...))

        :param path: the destination path
        :param kwargs: additional output arguments
        :return: the output
        :rtype: Path
        :raises ProcessingException: if any exception is captured during processing
        """
        ...
