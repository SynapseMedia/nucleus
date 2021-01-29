"""
Watchit simple and useful general purpose gateway framework

Always remember to comply with the specifications of
each resolver for the correct functioning of the gateway.

Define your resolvers modules below.
Ex: Each resolver must implement 2 fundamental methods.

class Dummy:
    def __init__(self, scheme)
        Initialize resolver with scheme module
        Scheme module define methods to validate and clean
        pass

    def __str__(self):
        return 'Test'

    def __call__(self, *args, **kwargs):
        return {}

"""
import inspect
import pkgutil

__title__ = 'watchit'
__version__ = '0.1.0'
__author__ = 'Geolffrey Mena'
__license__ = 'MIT'
__copyright__ = 'Copyright 2020-2021 Geolffrey MEna'


def load():
    """
    Auto load modules in `resolvers` path
    """
    for loader, name, is_pkg in pkgutil.walk_packages(__path__):
        _module = loader.find_module(name).load_module(name)
        for _, obj in inspect.getmembers(_module):
            if inspect.isclass(obj) and is_pkg and hasattr(obj, '__call__'):
                yield obj


__all__ = ['load']
