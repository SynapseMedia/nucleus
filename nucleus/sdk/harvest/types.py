from __future__ import annotations

# Convention for importing constants/types
from abc import ABC, abstractmethod

from nucleus.core.types import JSON, Iterator


class Collector(ABC):
    """Collector define an abstraction with methods needed to handle metadata collection process.
    Subclasses should implement the __iter__ method to collect metadata from various data inputs.
    Use this class to create collector subtypes.

    Usage:

        class File(Collector):

            def __iter__(self):
                # read our file and yield the content
                with open('dummy.json') as file:
                    for data in json.load(file):
                        yield JSON(data)

    """

    @abstractmethod
    def __iter__(self) -> Iterator[JSON]:
        """Collect metadata from any kind of data input and return an iterator.

        :return: The iterable JSON with data to process.
        """
        ...


__all__ = ('Collector',)
