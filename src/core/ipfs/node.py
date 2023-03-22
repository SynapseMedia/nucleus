from .types import ID
from .cmd import IPFS


def id() -> ID:
    """Return running ipfs node id
    :raises IPFSRuntimeException: if ipfs cmd execution fail
    """
    call = IPFS("/id")()
    return call.output.get("ID")
