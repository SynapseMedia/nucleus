from __future__ import annotations


# Convention for importing constants/types
from abc import ABC, abstractmethod
from nucleus.core.types import Iterator
from .model import Collection

class Collector(ABC):
    """Abstract class for collecting metadata.
    Collector define an "strict abstraction" with methods needed to handle metadata collection process.
    Subclasses should implement the __iter__ method to collect metadata from various data inputs.
    """

    def __str__(self) -> str:
        """Context name for current data.

        We use this context name to keep a reference to data.
        """
        return "__collectable__"

    @abstractmethod
    def __iter__(self) -> Iterator[Collection]:
        """Collect metadata from any kind of data input"""
        ...
