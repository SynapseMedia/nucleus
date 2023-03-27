from dataclasses import dataclass, field, asdict
from nucleus.core.http import LiveSession
from nucleus.core.types import Setting

from .constants import IPFS_API_ADD


@dataclass
class Add:
    """Add files or text to ipfs.
    Each input setting is expected to iter arguments for post requests
    ref: https://docs.ipfs.io/reference/cli/#ipfs-add
    """

    _input: Setting
    pin: bool = False
    quieter: bool = True
    hash: str = "blake2b-208"
    cid_version: int = field(metadata={"name": "cid-version"}, default=1)

    def __call__(self, session: LiveSession):
        # convert dataclass to request IPFS 'add endpoint' attributes.
        params = asdict(self)
        params.pop("_input")
        # convert input setting to adapt the behavior of the request. eg. send
        # raw data, upload files, etc
        compiled_settings = dict(self._input)
        # post request to /add endpoint using defined params and settings
        return session.post(IPFS_API_ADD, params=params, **compiled_settings)


__all__ = ("Add",)
