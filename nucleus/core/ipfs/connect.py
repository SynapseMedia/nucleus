import nucleus.core.http as http
from nucleus.core.types import Optional

from .constants import IPFS_DEFAULT_ENDPOINT
from .rpc import RPC


def rpc(endpoint: Optional[str] = None):
    """Create a new ipfs rpc interface object.
    The purpose of this method is to create a flexible factory that allows connect with diff endpoints.

    :param endpoint: the endpoint to connect to
    :return: a new ipfs api interface object
    :rtype: IPFSApi
    """
    endpoint = endpoint or IPFS_DEFAULT_ENDPOINT
    return RPC(http.live_session(endpoint))


__all__ = ('rpc',)
