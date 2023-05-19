from dataclasses import dataclass

import nucleus.core.dataclass as dc
from nucleus.core.http import LiveSession
from nucleus.core.types import Settings

from .constants import IPFS_API_BLOCK_PUT


@dataclass(slots=True)
class BlockPut:
    """Put data in block.
    ref: http://docs.ipfs.tech/reference/kubo/rpc/#api-v0-block-put
    """

    input: Settings
    mhtype: str = 'sha2-256'
    mhlen: int = -1
    pin: bool = True
    cid_codec: str = 'cidv2'
    allow_big_block: bool = False

    def __call__(self, session: LiveSession):
        # convert dataclass to request IPFS 'add endpoint' attributes.
        # we don't want `input` into params
        params = dc.asdict_sanitize(self, ('input',))
        compiled_settings = dict(self.input)
        # post request to /block/put endpoint using defined params and settings
        return session.post(IPFS_API_BLOCK_PUT, params=params, **compiled_settings)


__all__ = ('BlockPut',)
