import pkgutil
import inspect
import itertools


from collections import defaultdict
from src.core.types import Iterator, Any, Mapping
from .constants import COLLECTORS_PATH
from .types import Collector, Collection


def map(collectors: Iterator[Collector]) -> Mapping[str, Iterator[Collection]]:
    """Returns a map of collectors.
    Map collectors using name as key and the metadata content as value list.

    :param collectors: collector iterator
    :return: mapped collected data using the name of collector as key and value with meta provided.
    :rtype: Mapping[str, Iterator[Collection]]
    """

    mapped: Any = defaultdict(list)
    # For each collector metadata provided lets parse it and map it.
    for collected in collectors:
        mapped[str(collected)] += collected
    return mapped


def merge(collectors: Iterator[Collector]) -> Iterator[Collection]:
    """Returns merged collectors.

    :param collectors: Collector iterator
    :return: merged collectors
    :rtype: Iterator[Collection]
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
