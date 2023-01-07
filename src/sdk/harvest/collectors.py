# import inspect
import pkgutil
import inspect
import pydantic
import itertools


from collections import defaultdict
from src.core.types import Iterator, Type, T, Any, Dict
from .constants import COLLECTORS_PATH
from .types import Collector


def map_as(as_: Type[T], collectors: Iterator[Collector]) -> Dict[str, T]:
    """Returns mapped collected data as T.
    Map collectors using name as key and the metadata content as value list.
    ref: https://pydantic-docs.helpmanual.io/usage/models/#helper-functions

    :param collectors: Collector iterator
    :return: Mapped collected data using the name of collector as key and value with meta provided.
    :rtype: Dict[str, T]
    """

    mapped: Any = defaultdict(list)
    # For each collector metadata provided lets parse it and map it.
    for collected in collectors:
        parsed_obj = map(lambda x: pydantic.parse_obj_as(as_, x), collected)
        mapped[str(collected)] += parsed_obj
    return dict(mapped)


def merge_as(as_: Type[T], collectors: Iterator[Collector]) -> Iterator[T]:
    """Returns merged collected data as T.
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
