from __future__ import annotations


# Convention for importing constants/types
from enum import Enum
from abc import ABC, abstractmethod
from nucleus.core.types import Iterator, Dict, Any


class MediaType(Enum):
    # standard type names implementation
    VIDEO = "video"
    IMAGE = "image"


class Collector(ABC):
    """Abstract class for metadata collection.
    Collector define an "strict abstraction" with methods needed to handle metadata collection process.
    Subclasses should implement the __iter__ method to collect metadata from various data inputs.
    Use this class to create collector subtypes.
    """

    @abstractmethod
    def __iter__(self) -> Iterator[Dict[Any, Any]]:
        """Collect metadata from any kind of data input"""
        ...
