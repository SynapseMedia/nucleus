from __future__ import annotations

from jwcrypto import jwe, jwk, jws

from nucleus.core.types import Literal, Protocol, Raw, Setting, Union
from nucleus.sdk.storage import Object, Store

JWK = jwk.JWK
JWS = jws.JWS
JWE = jwe.JWE

Claims = Literal['s', 'd', 't']
JWT = Union[JWS, JWE]


class Metadata(Protocol):
    """Metadata defines the expected behavior of metadata types.
    Examples of metadata types include:

    - Descriptive
    - Structural
    - Technical

    """

    def __str__(self) -> Claims:
        """Metadata types MUST return the specified claims as a string.
        Examples of valid claims include:
            s, t, d

        :return: The claim type specified in SEP-001
        """
        ...


class Standard(Protocol):
    """Standard defines the expected behavior of the standard implementations according to SEP-001."""

    def header(self) -> Raw:
        """Return the standard header

        :return:
        """
        ...

    def payload(self) -> Raw:
        """Return the standard payload

        :return:
        """
        ...


class Serializer(Protocol):
    """Serializer specifies methods to handle serialization for
    each strategy according to the SEP-001 serialization spec.
    """

    def __str__(self) -> str:
        """Serialization as string.

        :return:
        """
        ...

    def __bytes__(self) -> bytes:
        """Serialization as bytes.

        :return:
        """
        ...

    def __iter__(self) -> Setting:
        """Yield `typ` headers specified in SEP-001 standard.

        :return: The iterable media type settings
        """
        ...

    def __init__(self, standard: Standard):
        """Serializer must be initialized with the SEP-001 standard implementation.

        :param standard: The standard implementation
        """
        ...

    def save_to(self, store: Store) -> Object:
        """Publishes serialization into the local store.

        :param store: The local store function
        :return: Object instance
        """

        ...

    def update(self, jwt: JWT) -> Serializer:
        """Receive updates when cryptographic operations are ready to be used.
        This step allows for adding a new state or performing operations on JWS/JWE to handle additional encoding.

        :param jwt: The type of JWT implementation to handle.
        :return: Self serializer
        """
        ...


class Keyring(Protocol):
    """Keyring specifies the required methods for handling
    keys based on the JWK (JSON Web Key) RFC 7517 standard.
    """

    def __iter__(self) -> Setting:
        """Yield `alg` and `jwk` headers specified in RFC 7517-7516 standard.

        :return: The iterable header settings to associate
        """
        ...

    def jwk(self) -> JWK:
        """Return the internal JWK (JSON Web Key) instance

        :return: The JWK (JSON Web Key) instance
        """
        ...

    def fingerprint(self) -> str:
        """Return the base64 decoded thumbprint as specified by RFC 7638

        :return: The decoded thumbprint as string. eg: sha256, blake, etc..
        """
        ...

    def from_dict(self, raw_key: Raw) -> Keyring:
        """Initialize Keyring using JWK JSON format

        :param raw_key: Keyring to import as dict (JSON format)
        :return: KeyRing object
        """
        ...

    def as_dict(self) -> Raw:
        """Export Keyring as JWK JSON format

        :return: Keyring as dict
        """
        ...


class Crypto(Protocol):
    """Crypto specifies a pub/sub middleware that handles cryptographic operations on serializers.
    It notifies serializers when crypto operations are ready to be used.
    """

    def __init__(self, serializer: Serializer):
        """Initialize with the serializer on which we will operate.

        :param serializer: The serializer implementation
        """
        ...

    def serialize(self) -> Serializer:
        """Notify the underlying serializer of the current state of the cryptographic operation.
        During this process, the serializer may modify its state or store the results of the cryptographic operations.

        :return: The input Serializer with a new ready to use state
        """
        ...

    def add_key(self, kr: Keyring) -> Crypto:
        """Bind keys to the serialization process.

        :param kr: Keyring to associate with operation
        :return: Crypto object
        """
        ...


__all__ = ()
