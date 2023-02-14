from abc import abstractmethod, ABCMeta
from src.core.types import Protocol


class Engine(Protocol, metaclass=ABCMeta):
    """Abstract middleware class class to handle standard actions for media processing.

    Any type of input, for example, video, image, music, etc., needs some type of processing to be transmitted or consumed.
    We could define any steps or logic needed to process our media.
    """

    @abstractmethod
    def __enter__(self):
        ...

    @abstractmethod
    def __exit__(self):
        ...
