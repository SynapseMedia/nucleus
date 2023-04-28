from __future__ import annotations

from dataclasses import dataclass
from nucleus.core.types import Optional, CID, Raw
from .types import Metadata

"""Standard implementation for SEP-001 .
ref: https://github.com/SynapseMedia/sep/blob/main/SEP/SEP-001.mdhttps://github.com/SynapseMedia/sep/blob/main/SEP/SEP-001.md
"""


"""
HS256	HMAC using SHA-256	Required
HS384	HMAC using SHA-384	Optional
HS512	HMAC using SHA-512	Optional
RS256	RSASSA-PKCS1-v1_5 using SHA-256	Recommended
RS384	RSASSA-PKCS1-v1_5 using SHA-384	Optional
RS512	RSASSA-PKCS1-v1_5 using SHA-512	Optional
ES256	ECDSA using P-256 and SHA-256	Recommended+
ES384	ECDSA using P-384 and SHA-384	Optional
ES512	ECDSA using P-521 and SHA-512	Optional
PS256	RSASSA-PSS using SHA-256 and MGF1 with SHA-256	Optional
PS384	RSASSA-PSS using SHA-384 and MGF1 with SHA-384	Optional
PS512	RSASSA-PSS using SHA-512 and MGF1 with SHA-512	Optional
none	No digital signature or MAC performed	Optional

"""


@dataclass
class Header:
    """JWT Header standard based on SEP-001:
    ref: https://github.com/SynapseMedia/sep/blob/main/SEP/SEP-001.md
    """

    # Is used by JWT applications to declare the media type [IANA.MediaTypes]
    # of this complete JWT
    typ: str
    # The "alg" (algorithm) Header Parameter identifies the cryptographic
    # algorithm used in signature creation
    alg: str = "HS256"


@dataclass(init=False)
class Payload:
    """JWT Payload standard based on SEP-001:
    ref: https://github.com/SynapseMedia/sep/blob/main/SEP/SEP-001.md
    """

    s: Raw  # s: structural metadata Object
    d: Raw  # d: descriptive metadata Object
    t: Optional[Raw] = None  # t: technical metadata Object
    r: Optional[CID] = None  # r: reserved for future use

    def add(self, meta: Metadata) -> None:
        """Associate metadata to payload.

        :param meta: the metadata type to store in payload
        :raises NotImplementedError if invalid metadata is added
        """
        setattr(self, str(meta), vars(meta))


@dataclass(slots=True)
class SEP001:
    """SEP-001 standard implementation:
    ref: https://github.com/SynapseMedia/sep/blob/main/SEP/SEP-001.md
    """

    header: Header
    payload: Payload

    def add_metadata(self, meta: Metadata):
        """Proxy add metadata to payload

        :param meta: the metadata type to store in payload
        :return: none
        :rtype: None
        """
        self.payload.add(meta)


__all__ = ["SEP001", "Payload", "Header"]
