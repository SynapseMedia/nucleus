from abc import abstractmethod, ABCMeta
from src.core.types import Protocol, Any, Path


class Engine(Protocol, metaclass=ABCMeta):
    """Abstract proxy adapter class to handle standard actions for media processing.

    Any type of input, for example, video, image, music, etc., needs some type of processing to be transmitted or consumed.
    We could define any steps or logic needed to process our media.
    """

    @abstractmethod
    def __init__(self, path: Path, **options: Any):
        """Initialize engine with media input path.
        
        :param path: the input media
        """
        ...

    def output(self, path: Path) -> Path:
        """Standard processed media output.

        eg.
            with Engine(Path(...)) as stream:
                ...more code here
                stream.output(Path(...))

        """
        ...

    def __getattr__(self, name: str) -> Any:
        """Delegate calls to any internal tool or library"""
