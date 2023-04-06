import functools

from .services import Estuary
from .constants import ESTUARY_API_BASE

# Ready to use estuary service
estuary = functools.partial(Estuary, ESTUARY_API_BASE)


__all__ = ("estuary",)
