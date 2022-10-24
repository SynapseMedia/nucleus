import inspect
import pkgutil


def load():
    """
    Find modules in `resolvers` path
    """
    for loader, name, is_pkg in pkgutil.walk_packages(__path__):
        _module = loader.find_module(name).load_module(name)
        for _, obj in inspect.getmembers(_module):
            if inspect.isclass(obj) and is_pkg:
                yield obj


__all__ = ["load"]
