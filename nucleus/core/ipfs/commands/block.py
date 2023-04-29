import dataclasses

from dataclasses import dataclass, field
from nucleus.core.types import Setting, CID
from nucleus.core.http import LiveSession

from .constants import IPFS_API_BLOCK_PUT, IPFS_API_BLOCK_GET


@dataclass(slots=True)
class Put:
    """Put text in ipfs block.
    ref: http://docs.ipfs.tech.ipns.localhost:8080/reference/kubo/rpc/#api-v0-block-put
    """

    input: Setting
    mhtype: str = "sha2-256"
    mhlen: int = -1
    pin: bool = True
    cid_codec: str = field(metadata={"name": "cid-codec"}, default="cidv2")
    allow_big_block: bool = field(
        metadata={
            "name": "allow-big-block"},
        default=False)

    def __call__(self, session: LiveSession):
        # convert dataclass to request IPFS 'add endpoint' attributes.
        params = dataclasses.asdict(self)
        params.pop("input", None)
        compiled_settings = dict(self.input)
        # post request to /add endpoint using defined params and settings
        return session.post(
            IPFS_API_BLOCK_PUT,
            params=params,
            **compiled_settings)


@dataclass(slots=True)
class Get:
    """Get block from ipfs.
    ref: http://docs.ipfs.tech.ipns.localhost:8080/reference/kubo/rpc/#api-v0-block-get
    """

    arg: CID

    def __call__(self, session: LiveSession):
        params = dataclasses.asdict(self)
        return session.post(IPFS_API_BLOCK_GET, params=params)


@dataclass(slots=True)
class Remove:
    """Remove block from ipfs.
    ref: http://docs.ipfs.tech.ipns.localhost:8080/reference/kubo/rpc/#api-v0-block-rm
    """

    arg: CID
    force: bool = False
    quiet: bool = False

    def __call__(self, session: LiveSession):
        params = dataclasses.asdict(self)
        return session.post(IPFS_API_BLOCK_GET, params=params)


__all__ = ("Put", "Get", "Remove")
