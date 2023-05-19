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

    :param collectors: collector iterator
    :return: mapped collected data using the name of collector as key and value with meta provided.
    :rtype: Mapping[str, Iterator[JSON]
    """

    mapped: Any = defaultdict(list)
    # For each collector metadata provided lets parse it and map it.
    for collected in collectors:
        mapped[type(collected).__name__] += collected
    return mapped


def merge(collectors: Iterator[Collector]) -> Iterator[JSON]:
    """Returns merged collectors.

    :param collectors: Collector iterator
    :return: merged collectors
    :rtype: Iterator[JSON]
    """

    return itertools.chain.from_iterable(collectors)


def load(path: str = COLLECTORS_PATH) -> Iterator[Collector]:
    """Import submodules from a given path and yield module object

    :param path: the path to search for submodules.
    :return: iterator of matched modules.
    :rtype: Iterator[Collector]
    """

    for module_finder, name, _ in pkgutil.iter_modules([path]):
        module = module_finder.find_module(name).load_module(name)  # type: ignore

        # Get the module collector class
        for _, obj in inspect.getmembers(module):
            if not inspect.isabstract(obj) and inspect.isclass(obj):
                if issubclass(obj, Collector):
                    yield obj()  # yield an instance of collector


__all__ = ('load', 'map', 'merge')
