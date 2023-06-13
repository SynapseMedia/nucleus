from __future__ import annotations

from jwcrypto import jwe, jwk, jws

from nucleus.core.types import Literal, Protocol, Raw, Setting, Union
from nucleus.sdk.storage import Object, Store

JWK = jwk.JWK
JWS = jws.JWS
JWE = jwe.JWE

Claims = Literal['s', 'd', 't']
Operations = Union[JWS, JWE]


class Metadata(Protocol):
    """Metadata defines the expected behavior of metadata types.
    Examples of metadata types include:

    - Descriptive
    - Structural
    - Technical

    """

    def __str__(self) -> Claims:
        """Metadata types MUST return the specified claims as a string.
        Examples of valid claims include: s, t, d
        """
        ...


class Standard(Protocol):
    """Standard defines the expected behavior of Standard implementations.
    ref: https://github.com/SynapseMedia/sep/blob/main/SEP/SEP-001.md
    """

    def header(self) -> Raw:
        """Return the standard header"""
        ...

    def payload(self) -> Raw:
        """Return the standard payload"""
        ...


class Serializer(Protocol):
    """Serializer observer specifies the methods needed to handle SEP001 serialization.
    Defines how to handle serialization for each strategy according to the specification, which includes:

    - Compact
    - DAG-JOSE

    This template class must be implemented by other classes that provide concrete serialization logic.
    ref: https://github.com/SynapseMedia/sep/blob/main/SEP/SEP-001.md
    """

    def __str__(self) -> str:
        """The serialized data as string"""
        ...

    def __bytes__(self) -> bytes:
        """The payload data ready to sign/encrypt"""
        ...

    def __iter__(self) -> Setting:
        """Expected to use to provide additions to the header registry"""
        ...

    def __init__(self, standard: Standard):
        """Serializer must be initialized with Standard implementation"""
        ...

    def save_to(self, store: Store) -> Object:
        """Could be used to store assets.
        eg. After generate CID from payload dag-cbor we need to store the bytes into blocks
        """

        ...

    def update(self, jwt: Operations) -> Serializer:
        """Receive updates when serialization is ready to handle any additional encoding step.
        In this step we could add a new state or operate over JWS/JWE to handle any additional encoding.

        :param jwt: JWT to handle
        :return: ready to use Serializer
        """
        ...


class Keyring(Protocol):
    """Keyring specifies the required methods for handling keys based on the JWK (JSON Web Key) RFC 7517 standard"""

    def __iter__(self) -> Setting:
        """Yield needed headers to add into signature/recipient"""
        ...

    def jwk(self) -> JWK:
        """Return the internal JWK (JSON Web Key) instance"""
        ...

    def fingerprint(self) -> str:
        """Return the base64 decoded thumbprint as specified by RFC 7638"""
        ...

    def from_dict(self, raw_key: Raw) -> Keyring:
        """Initialize Keyring from JWK standard JSON format"""
        ...

    def as_dict(self) -> Raw:
        """Export Keyring as JWK in standard JSON format"""
        ...


class Crypto(Protocol):
    """Specify a pub/sub middleware that handle cryptographic operations on serializers"""

    def __init__(self, serializer: Serializer):
        """Initialize with the serializer on which we will operate"""
        ...

    def serialize(self) -> Serializer:
        """Notify the underlying serializer of the current state of the cryptographic operation.
        During this process, the serializer may modify its state or store the results of the operations.
        """
        ...

    def add_key(self, kr: Keyring) -> Crypto:
        """Bind keys to the serialization process.

        :param kr: Keyring to associate with operation
        :return: Crypto object
        """
        ...


__all__ = ()
