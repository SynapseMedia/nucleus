import nucleus.core.exceptions as exceptions

from dataclasses import dataclass
from nucleus.core.http import LiveSession
from nucleus.core.types import Path
from .constant import IPFS_API_ADD


@dataclass
class Directory:
    """Add directory to ipfs.
    ref: https://docs.ipfs.io/reference/cli/#ipfs-add
    """

    path: Path

    def __call__(self, session: LiveSession):
        if not self.path.exists():
            raise exceptions.IPFSRuntimeError(
                f"raised trying to execute `add` directory with an invalid path {self.path}"
            )

        return session.post(
            IPFS_API_ADD,
            data=dict(self),
            files={"file": self.path.read_bytes()},
        )

    def __iter__(self):
        yield "recursive", "true",
        yield "quieter", "true",
        yield "cid-version", "1"
        yield "pin", "false"
        yield "hash", "blake2b-208"
