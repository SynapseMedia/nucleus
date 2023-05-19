from __future__ import annotations

# Convention for importing constants/types
from abc import ABC, abstractmethod

from nucleus.core.types import JSON, Iterator


class Collector(ABC):
    """Abstract class for metadata collection.
    Collector define an abstraction with methods needed to handle metadata collection process.
    Subclasses should implement the __iter__ method to collect metadata from various data inputs.
    Use this class to create collector subtypes.
    """

    @abstractmethod
    def __iter__(self) -> Iterator[JSON]:
        """Collect metadata from any kind of data input"""
        ...


__all__ = ('Collector',)
