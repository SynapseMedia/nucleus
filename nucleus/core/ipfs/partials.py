import functools
from .api import IPFSApi
from .constants import IPFS_DEFAULT_ENDPOINT

# ready to use api with default ipfs api endpoint
api = functools.partial(IPFSApi, IPFS_DEFAULT_ENDPOINT)

__all__ = ("api",)
