import pkgutil
import inspect
import itertools
import builtins


from collections import defaultdict
from src.core.types import Iterator, Any, Mapping, Union
from .constants import COLLECTORS_PATH
from .types import Collector, Model


def batch_save(e: Iterator[Model]) -> Iterator[Union[int, None]]:
    """Exec batch insertion into database
    WARN: This execution its handled by a loop

    :param e: Entries to insert into database.
    :return: Iterator with a boolean flag for each operation.
    :rtype: Iterator[bool]
    """
    return builtins.map(lambda x: x.save(), e)


def map(collectors: Iterator[Collector]) -> Mapping[str, Iterator[Model]]:
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
    return mapped


def merge(collectors: Iterator[Collector]) -> Iterator[Model]:
    """Returns merged collectors.
    ref: https://pydantic-docs.helpmanual.io/usage/models/#helper-functions

    :param collectors: Collector iterator
    :return: Merged collectors
    :rtype: MetaIter
    """

    return itertools.chain.from_iterable(collectors)


def load(path: str = COLLECTORS_PATH) -> Iterator[Collector]:
    """Import submodules from a given path and yield module object

    :param path: The path to search for submodules.
    :return: Iterator of matched modules.
    :rtype: Iterator[Collector]
    """

    for module_finder, name, _ in pkgutil.iter_modules([path]):
        module = module_finder.find_module(
            name).load_module(name)  # type: ignore

        # Get the module collector class
        for _, obj in inspect.getmembers(module):
            if not inspect.isabstract(obj) and inspect.isclass(obj):
                if issubclass(obj, Collector):
                    yield obj()  # yield an instance of collector
