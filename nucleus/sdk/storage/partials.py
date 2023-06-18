import functools

from .constants import ESTUARY_API_BASE
from .services import Estuary

# Ready to use estuary service
estuary = functools.partial(Estuary, ESTUARY_API_BASE)


__all__ = ('estuary',)
