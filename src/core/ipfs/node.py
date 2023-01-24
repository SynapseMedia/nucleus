from src.core.types import ID
from .cmd import CLI


def id() -> ID:
    """Return running ipfs node id"""
    call = CLI("/id")()
    return call.output.get("ID")
