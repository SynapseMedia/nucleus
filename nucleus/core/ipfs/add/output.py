from dataclasses import dataclass

from nucleus.core.types import CID


@dataclass
class Stored:
    """Represents ipfs /add output"""

    cid: CID
    name: str
    size: float


__all__ = ("Stored",)
