from nucleus.core.types import Protocol, Literal
from jwcrypto import jwk, jws, jwe

Claims = Literal["s", "d", "t"]

JWK = jwk.JWK
JWS = jws.JWS
JWE = jwe.JWE


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


__all__ = ()
