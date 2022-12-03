# import inspect
import pkgutil
import inspect
import itertools

from src.core.types import Iterator
from .constants import COLLECTORS_PATH
from .types import Collector
from .models import Movie


def merge(collectors: Iterator[Collector]) -> Iterator[Movie]:
    """Returns merged collected data as Movie iterator.
    Collected data is merged and later used to instantiate Movie model.
    ref: https://pydantic-docs.helpmanual.io/usage/models/#helper-functions

    :param collectors: Collector iterator
    :return: Merged collectors
    :rtype: Iterator[Movie]
    """
    collected = itertools.chain.from_iterable(collectors)
    return map(Movie.parse_obj, collected)


def load(path: str = COLLECTORS_PATH) -> Iterator[Collector]:
    """Import submodules from a given path and yield module object

    :param path: The path to search for submodules.
    :return: Iterator of matched modules.
    :rtype: Iterator[Collector]
    """

    for module_finder, name, _ in pkgutil.iter_modules([path]):
        module = module_finder.find_module(name).load_module(name)  # type: ignore

        # Get the module collector class
        for _, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                yield obj()
