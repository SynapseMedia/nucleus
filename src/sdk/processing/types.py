from abc import abstractmethod, ABCMeta
from src.core.types import Protocol, Any, Path


class Engine(Protocol, metaclass=ABCMeta):
    """Abstract middleware class class to handle standard actions for media processing.

    Any type of input, for example, video, image, music, etc., needs some type of processing to be transmitted or consumed.
    We could define any steps or logic needed to process our media.
    """

    @abstractmethod
    def __init__(self, media: Path):
        """Initialize engine with any media path."""
        ...

    @abstractmethod
    def __enter__(self):
        """Defines what the context manager should do at the beginning of the block created by the with statement."""
        ...

    @abstractmethod
    def __call__(self, *options: Any):
        """Execute any action over media proxy using instructions
        eg.
            engine = Engine(Media("image.png"))
            engine(Instruction(method, params))
        """
        ...

    @abstractmethod
    def __exit__(self):
        """Defines what the context manager should do after its block has been executed (or terminates)"""
        ...
