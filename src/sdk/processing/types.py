from __future__ import annotations

from abc import abstractmethod, ABC
from src.sdk.harvest.model import Media
from src.core.types import (
    Any,
    Path,
    URL,
    Union,
    Callable,
    Adapter,
    Generic,
    T,
)


# Alias for allowed engine inputs
Processable = Media[Union[Path, URL]]


class Engine(ABC, Generic[T]):
    """Engine implements a media engine template that uses an underlying library as interface to process media files and produce output.
    The engine adapt dynamically the library so that methods can be directly accessed and process media in a specific context.
    """

    _library: Adapter[T]

    def __init__(self, interface: Adapter[T]):
        """Template method initialize engine with media input path.

        :param interface: adaptable interface
        :param type: engine type
        :return: engine instance
        :rtype: Engine
        """
        self._library = interface

    def __getattr__(self, name: str) -> Callable[[Any], Any]:
        """Control behavior for when a user attempts to access an attribute that doesn't exist.
        This method delegate the call to any underlying tool or library.

        :return: expected method to call
        :rtype: Callable[[Any], Any]
        :raise ValueError if accessed attribute is not callable
        """

        method = getattr(self._library, name)
        if not callable(method):
            raise ValueError("expected call to underlying method")

        # return callable
        return method

    def annotate(self, name: str, *args: Any, **kwargs: Any) -> Engine[T]:
        """It allow chain calls for underlying methods keeping object reference.

        :param name: the name of the method to call
        :param kwargs: additional keyword arguments
        :return: annotated engine
        :rtype: Engine
        """

        # concat `fluent interface`
        call = getattr(self, name)
        result = call(*args, **kwargs)
        # keep chaining if result method is same object
        if isinstance(result, self._library):  # type: ignore
            self._library(result)
        return self

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
