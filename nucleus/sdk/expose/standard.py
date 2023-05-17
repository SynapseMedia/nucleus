from __future__ import annotations

from dataclasses import dataclass
from nucleus.core.types import Raw, Optional, CID

from .types import Metadata

"""Standard implementation for SEP-001 .
ref: https://github.com/SynapseMedia/sep/blob/main/SEP/SEP-001.mdhttps://github.com/SynapseMedia/sep/blob/main/SEP/SEP-001.md
"""


@dataclass
class Header:
    """JWT Header standard based on SEP-001:
    ref: https://github.com/SynapseMedia/sep/blob/main/SEP/SEP-001.md
    """

    # Is used by JWT applications to declare the media type [IANA.MediaTypes]
    # of this complete JWT
    typ: str


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

    def add_metadata(self, meta: Metadata) -> SEP001:
        """Proxy add metadata to payload

        :param meta: the metadata type to store in payload
        :return: none
        :rtype: None
        """
        self.payload.add(meta)
        return self
