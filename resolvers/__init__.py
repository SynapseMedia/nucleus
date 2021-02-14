"""
Watchit simple and useful general purpose gateway framework

Always remember to comply with the specifications of
each resolver for the correct functioning of the gateway.

Define your resolvers modules below.
Ex: Each resolver must implement 3 fundamental methods.

class Dummy:
    def __str__(self) -> str:
        return 'Test'

    def __call__(self, *args, **kwargs) -> iter:
        yield data

"""
import inspect
import pkgutil

__title__ = 'watchit'
__version__ = '0.1.0'
__license__ = 'MIT'
__copyright__ = 'Copyright 2020-2021 ZorrillosDev'


def load():
    """
    Auto load modules in `resolvers` path
    """
    for loader, name, is_pkg in pkgutil.walk_packages(__path__):
        _module = loader.find_module(name).load_module(name)
        for _, obj in inspect.getmembers(_module):
            if inspect.isclass(obj) and is_pkg:
                yield obj


__all__ = ['load']
