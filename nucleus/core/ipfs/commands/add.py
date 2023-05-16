import nucleus.core.dataclass as dc

from dataclasses import dataclass, field
from nucleus.core.types import Setting
from nucleus.core.http import LiveSession

from .constants import IPFS_API_ADD


@dataclass(slots=True)
class Add:
    """Add files or text to ipfs.
    Each input setting is expected to iter arguments for post requests
    ref: https://docs.ipfs.io/reference/cli/#ipfs-add
    """

    input: Setting
    pin: bool = False
    quieter: bool = True
    hash: str = "blake2b-208"
    cid_version: int = field(metadata={"name": "cid-version"}, default=1)

    def __call__(self, session: LiveSession):
        # convert dataclass to request IPFS 'add endpoint' attributes.
        # we don't want `input` into params
        params = dc.asdict_exclusive(self, ("input",))
        compiled_settings = dict(self.input)
        # post request to /add endpoint using defined params and settings
        return session.post(IPFS_API_ADD, params=params, **compiled_settings)


__all__ = ("Add",)
