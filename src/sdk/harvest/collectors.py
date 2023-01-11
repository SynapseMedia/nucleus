import pkgutil
import inspect
import pydantic
import itertools
import builtins


from collections import defaultdict
from src.core.types import Iterator, Any, Type, T
from .constants import COLLECTORS_PATH
from .types import Collectors, MetaIter, MetaMap


def parse(as_: Type[T], meta: MetaIter) -> Iterator[T]:
    """Return parsed metadata as T type.
     
    :param as_: Model to parse metadata
    :param meta: The raw metadata input
    :return: The parsed metadata
    :rtype: Iterator[T]
    """
    return builtins.map(lambda x: pydantic.parse_obj_as(as_, x), meta)


def map(collectors: Collectors) -> MetaMap:
    """Returns mapped collectors.
    Map collectors using name as key and the metadata content as value list.
    ref: https://pydantic-docs.helpmanual.io/usage/models/#helper-functions

    :param collectors: Collector iterator
    :return: Mapped collected data using the name of collector as key and value with meta provided.
    :rtype: MetaMap
    """

    mapped: Any = defaultdict(list)
    # For each collector metadata provided lets parse it and map it.
    for collected in collectors:
        mapped[str(collected)] += collected
    return dict(mapped)


def merge(collectors: Collectors) -> MetaIter:
    """Returns merged collectors.
    ref: https://pydantic-docs.helpmanual.io/usage/models/#helper-functions

    :param collectors: Collector iterator
    :return: Merged collectors
    :rtype: MetaIter
    """

    return itertools.chain.from_iterable(collectors)


def load(path: str = COLLECTORS_PATH) -> Collectors:
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
