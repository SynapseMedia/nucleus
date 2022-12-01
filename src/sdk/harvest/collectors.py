# import inspect
import pkgutil
import inspect
import itertools

from src.core.types import Iterator, Tuple, Dict
from .constants import COLLECTORS_PATH
from .types import Collector
from .models import Movie



def hashmap(collectors: Iterator[Collector]) -> Dict[str, Tuple[Movie]]:
    """Iterate over collectors and create a key value based on collector name

    :param collectors: Collectors object iterator
    :returns: Key value pairs for each collector
    :rtype: Dict[str, Dict[Any, Any]]
    """
    ...


def merge(collectors: Iterator[Collector]) -> Iterator[Movie]:
    """Iterate over collectors and merge results

    :param collectors: Collectors object iterator
    :returns: Merged collected as Movie iterator
    :rtype: Iterator[Dict[Any, Any]]
    """
    collected = itertools.chain.from_iterable(collectors)
    return map(Movie.parse_obj, collected)  # type: ignore


def load(path: str = COLLECTORS_PATH) -> Iterator[Collector]:
    """Import submodules from a given path and yield module object

    :param path: The path to search for submodules.
    :returns: Iterator of matched modules.
    :rtype: Iterator[Any]
    """

    for module_finder, name, _ in pkgutil.iter_modules([path]):
        module = module_finder.find_module(name).load_module(name)  # type: ignore

        # Get the module collector class
        for _, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                yield obj()
