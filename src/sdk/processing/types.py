from __future__ import annotations

from abc import abstractmethod, ABC
from src.core.types import Any, Path, Dict
from src.sdk.harvest.model import Media


class Engine(ABC):
    """Adapter/Template engine to handle standard actions for media processing.

    Any type of input, for example, video, image, music, etc., needs some type of processing to be transmitted or consumed.
    We could define any steps or logic needed to process our media.
    """

    _type: str
    _path: Path
    _input: Any
    _options: Dict[str, Any]

    def __init__(self, media: Media):
        """Template method initialize engine with media input path."""
        self._path = Path(media.route)
        self._type = media.type
        self._options = {}  # we could ad any default options here

    def __call__(self, **options: Any) -> Engine:
        """Template method to add options to the processing context.
        :param options: additional keyword arguments
        eg.

        engine = Engine(Path(..))
        with engine(max_muxing_queue_size=10) as video:
            ...
        """
        self._options = options
        return self

    def __exit__(self, *args: Any):
        """ Template method to handle context exit. Default is do nothing.
        Defines what the context manager should do after its block has been executed (or terminates)"""
        ...

    @abstractmethod
    def __enter__(self) -> Engine:
        """Defines what the context manager should do at the beginning of the block created by the with statement."""
        ...

    def annotate(self, name: str, *args: Any, **kwargs: Any) -> Engine:
        """Delegate calls to any underlying tool or library.
        It Allow chain underlying methods keeping object reference.
        
        :param name: the name of the attribute or method to call
        :param kwargs: additional keyword arguments
        :return: annotated engine
        :rtype: Engine
        """

        method = getattr(self._input, name)
        if not callable(method):
            assert ValueError("annotation can be used only with underlying methods")

        # concat `fluent interface`
        result = method(*args, **kwargs)
        if result is not None:
            self._input = result
        return self
    
    @abstractmethod
    def output(self, path: Path) -> Media:
        """Standard processed media output.
        Expected call output to get resulting File output.

        eg.
            with Engine(Path(...)) as stream:
                ...more code here
                stream.output(Path(...))

        :param path: the destination path
        :return: the output
        :rtype: Path
        """
        ...
