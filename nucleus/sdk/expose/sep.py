from __future__ import annotations

from dataclasses import dataclass

from nucleus.core.types import CID, Optional, Raw, Type

from .crypto import Sign
from .key import KeyRing
from .marshall import DagJose
from .types import Metadata, Serializer

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

    _header: Header
    _payload: Payload
    # serialization method eg. DagJose, Compact, etc
    _method: Type[Serializer] = DagJose

    def header(self) -> Raw:
        return vars(self._header)

    def payload(self) -> Raw:
        return vars(self._payload)

    def set_method(self, method: Type[Serializer]):
        """Set the serialization method.

        :param method: the serialization method
        :return: none
        :rtype: None
        """
        self._method = method

    def sign(self, key: KeyRing) -> Serializer:
        """Sign SEP using defined key and serialization method.

        :param key: the key to use during sign process
        :return: signed serializer
        :rtype: Serializer
        """
        serializer = self._method(self)
        sign = Sign(serializer).add_key(key)
        signed_serializer = sign.serialize()
        return signed_serializer

    def add_metadata(self, meta: Metadata) -> None:
        """Proxy add metadata to payload

        :param meta: the metadata type to store in payload
        :return: none
        :rtype: None
        """
        self._payload.add(meta)


__all__ = ('SEP001', 'Header', 'Payload')
