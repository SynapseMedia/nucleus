"""
Watchit simple and useful general purpose gateway framework

Always remember to comply with the specifications of
each resolver for the correct functioning of the gateway.

Define your resolvers below.
Ex: Each resolver must implement 2 fundamental methods.

class Test:
    def __str__(self):
        return 'Test'

    def __call__(self, *args, **kwargs):
        return {}

"""

__title__ = 'watchit'
__version__ = '0.1.0'
__author__ = 'Geolffrey Mena'
__license__ = 'MIT'
__copyright__ = 'Copyright 2020-2021 Geolffrey MEna'

from .yts import YTS
from .test import Test

RESOLVERS = [YTS, Test]
