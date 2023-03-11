from __future__ import annotations

from abc import abstractmethod, ABC
from src.core.types import Any, Path, URL, Mapping, Union, Adaptable
from src.sdk.harvest.model import Media

# Alias for allowed engine inputs
Processable = Media[Union[Path, URL]]


class Engine(ABC):
    """Template defines a media engine that uses an underlying library as interface to process media files and produce output.
    The engine adapt dynamically the library so that methods can be directly accessed and process media in a specific context.
    """

    _type: str
    _path: Path
    _interface: Adaptable
    _options: Mapping[str, Any]

    def __init__(self, media: Processable, **kwargs: Any):
        """Template method initialize engine with media input path.

        :param media: input media as URL or local Path
        :param kwargs: input options
        :return: engine instance
        :rtype: Engine
        """
        self._path = Path(media.route)
        self._type = media.type
        self._options = kwargs  # we could add any input options here

    def __exit__(self, *args: Any):
        """Template method to handle context exit. Default is do nothing.
        Defines what the context manager should do after its block has been executed (or terminates)"""
        ...

    def __getattr__(self, name: str) -> Any:
        """Delegate calls to any underlying tool or library.

        :param name: the name of the method to call
        :return: underlying method to call
        :rtype: Any
        :raise ValueError if accessed attribute is not callable
        """

        method = getattr(self._interface, name)
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
        result = call(*args, **kwargs)
        # keep chaining if result method is same object
        if isinstance(result, self._interface):  # type: ignore
            self._interface.__chaining__(result)
        return self

    @abstractmethod
    def __enter__(self) -> Engine:
        """Defines what the context manager should do at the beginning of the block created by the with statement.
        We can define in this step the input library for the engine.
        """
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
