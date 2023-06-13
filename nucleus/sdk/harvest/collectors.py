import inspect
import itertools
import pkgutil
from collections import defaultdict

from nucleus.core.types import JSON, Any, Iterator, Mapping

from .constants import COLLECTORS_PATH
from .types import Collector


def map(collectors: Iterator[Collector]) -> Mapping[str, Iterator[JSON]]:
    """Returns a map of collectors.
    Map collectors using name as key and the metadata content as value list.

    :param collectors: Collector iterator
    :return: Mapped collected data using the name of collector as key and value with meta provided.
    """

    mapped: Any = defaultdict(list)
    # For each collector metadata provided lets parse it and map it.
    for collected in collectors:
        mapped[type(collected).__name__] += collected
    return mapped


def merge(collectors: Iterator[Collector]) -> Iterator[JSON]:
    """Returns merged collectors.

    :param collectors: Collector iterator
    :return: Merged collectors
    """

    return itertools.chain.from_iterable(collectors)


def load(path: str = COLLECTORS_PATH) -> Iterator[Collector]:
    """Import submodules from a given path and yield module object.

    :param path: The path to search for submodules.
    :return: Iterator of matched modules.
    """

    for module_finder, name, _ in pkgutil.iter_modules([path]):
        found_module = module_finder.find_module(name)  # type: ignore
        # if not module loader available just continue
        if not found_module:
            continue

        module = found_module.load_module(name)
        # Get the module collector class
        for _, obj in inspect.getmembers(module):
            if not inspect.isabstract(obj) and inspect.isclass(obj):
                if issubclass(obj, Collector):
                    yield obj()  # yield an instance of collector


__all__ = ('load', 'map', 'merge')
