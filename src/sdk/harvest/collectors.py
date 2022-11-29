# import inspect
import pkgutil
import inspect
from src.core.types import Generator, Any
from .constants import COLLECTORS_PATH

def submodules(path: str = COLLECTORS_PATH) -> Generator[Any, Any, Any]:
    """Import submodules from a given path and return module object

    :param path: The path to search for submodules.
    :returns: Generator of matched modules.
    :rtype: Generator[Any, Any, Any]
    """
    
    for module_finder, name, _ in pkgutil.iter_modules([path]):
        module = module_finder.find_module(name).load_module(name)  # type: ignore

        # Get the module collector class
        for _, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                yield obj


