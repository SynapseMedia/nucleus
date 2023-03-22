from nucleus.core.types import Literal, URL
from nucleus.core.ipfs import Service
from .constants import ESTUARY_API_BASE


class EstuarySvc(Service):
    name: Literal["estuary"] = "estuary"
    endpoint: URL = URL(ESTUARY_API_BASE)


__all__ = ("EstuarySvc",)
