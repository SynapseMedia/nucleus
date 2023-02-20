from abc import abstractmethod, ABCMeta
from src.core.types import Protocol, Any, Path


class Engine(Protocol, metaclass=ABCMeta):
    """Abstract middleware class to handle standard actions for media processing.

    Any type of input, for example, video, image, music, etc., needs some type of processing to be transmitted or consumed.
    We could define any steps or logic needed to process our media.
    """

    @abstractmethod
    def __init__(self, path: Path):
        """Initialize engine with any media path."""
        ...

    @abstractmethod
    def __enter__(self):
        """Defines what the context manager should do at the beginning of the block created by the with statement."""
        ...

    @abstractmethod
    def __call__(self, **options: Any):
        """Add options to the processing context

        eg.

        engine = Engine(Path(..))
        with engine(max_muxing_queue_size=10) as video:
            ...
        """
        ...

    def __getattr__(self, name: str) -> Any:
        """Delegate calls to any internal processing logic"""

    @abstractmethod
    def __exit__(self):
        """Defines what the context manager should do after its block has been executed (or terminates)"""
        ...
