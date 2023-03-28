import functools
import nucleus.core.http as http

from nucleus.core.types import Optional

from .api import IPFSApi
from .constants import IPFS_DEFAULT_ENDPOINT


def _api_factory(endpoint: Optional[str] = IPFS_DEFAULT_ENDPOINT):
    """Create a new ipfs api interface object.
    The purpose of this method is to create a flexible factory that allows connect with diff endpoints.
    
    :param endpoint: the endpoint to connect to
    :return: a new ipfs api interface object
    :rtype: IPFSApi
    """
    return IPFSApi(http.live_session(endpoint))


api = functools.partial(_api_factory)

__all__ = ("api",)
