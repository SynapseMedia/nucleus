from .types import ID
from .cmd import IPFS


def id() -> ID:
    """Return running ipfs node id"""
    call = IPFS("/id")()
    return call.output.get("ID")
