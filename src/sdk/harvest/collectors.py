# import inspect
import pkgutil
import inspect
import itertools

from src.core.types import Iterator, Any, Dict
from .constants import COLLECTORS_PATH
from .types import Collector


def map(collectors: Iterator[Collector]):
    """Iterate over collectors and create a hash value for each collector"""
    ...
    
def merge(collectors: Iterator[Collector]) -> Iterator[Dict[Any, Any]]:
    """Iterate over collectors and merge results

    :param collectors: Obtained data from collectors iterators
    :return: Merged collectors results
    :rtype: List[Dict[Any, Any]]
    """

    return itertools.chain.from_iterable(collectors)


def load(path: str = COLLECTORS_PATH) -> Iterator[Any]:
    """Import submodules from a given path and return module object

    :param path: The path to search for submodules.
    :returns: Generator of matched modules.
    :rtype: Iterator[Any]
    """

    for module_finder, name, _ in pkgutil.iter_modules([path]):
        module = module_finder.find_module(name).load_module(name)  # type: ignore

        # Get the module collector class
        for _, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                yield obj()
