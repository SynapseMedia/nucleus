from dataclasses import dataclass
from nucleus.core.types import CID, Optional


@dataclass
class S:
    cid: CID
    path: Optional[str] = ""


@dataclass
class D:
    name: str
    desc: str


@dataclass
class T:
    size: int
    width: int
    height: int
    codec: str
    length: str


@dataclass
class Header:
    # Is used by JWT applications to declare the media type [IANA.MediaTypes]
    # of this complete JWT
    typ: str
    # The "alg" (algorithm) Header Parameter identifies the cryptographic
    # algorithm used in signature creation
    alg: str = "HS256"


@dataclass
class Payload:
    s: S  # s: structural metadata CID
    d: D  # d: descriptive metadata CID
    t: T  # t: technical metadata CID
