# import inspect
import pkgutil
import inspect
import pydantic
import itertools


from src.core.types import Iterator, Type, T
from .constants import COLLECTORS_PATH
from .types import Collector


def parse(collectors: Iterator[Collector], as_: Type[T]) -> Iterator[T]:
    """Returns merged collected data as Movie iterator.
    ref: https://pydantic-docs.helpmanual.io/usage/models/#helper-functions

    :param collectors: Collector iterator
    :return: Merged collectors as T
    :rtype: Iterator[T]
    """

    collected = itertools.chain.from_iterable(collectors)
    return map(lambda x: pydantic.parse_obj_as(as_, x), collected)


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
