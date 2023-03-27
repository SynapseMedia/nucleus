from dataclasses import dataclass
from nucleus.core.types import CID


@dataclass
class Impulse:
    v: float  # version
    sig: str  # signature
    pk: str  # public key
    media: CID  # media cid (meta for media resources)
    meta: CID  # metadata cid (metadata structure)
