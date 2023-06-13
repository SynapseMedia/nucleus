import nucleus.core.http as http
from nucleus.core.types import Optional

from .constants import IPFS_DEFAULT_ENDPOINT
from .rpc import RPC


def rpc(endpoint: Optional[str] = None) -> RPC:
    """Create a new IPFS RPC interface object.

    :param endpoint: The endpoint to attach the RPC.
    :return: A new IPFS API interface object.
    """
    endpoint = endpoint or IPFS_DEFAULT_ENDPOINT
    return RPC(http.live_session(endpoint))


__all__ = ('rpc',)
