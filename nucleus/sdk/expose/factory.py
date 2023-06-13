from nucleus.core.types import Any

from .key import Algorithm, Curve, KeyType, SignKeyRing, Use
from .sep import SEP001, Header, Payload


def standard(type: str) -> SEP001:
    """SEP001 factory

    :param type: The type of media to expose
    :return: New standard implementation sep-001 object
    """

    return SEP001(
        Header(type),
        Payload(),
    )


def es256(**kwargs: Any) -> SignKeyRing:
    """Return a KeyRing with ECDSA settings based on JWA specification.
    ref: https://www.rfc-editor.org/rfc/rfc7518#section-3.1

    :param kwargs: Any extra settings could be passed as keyword arguments
    :return: Ready to use signature keyring
    """

    return SignKeyRing(
        alg=Algorithm.ES256,
        key_type=KeyType.EllipticCurve,
        curve=Curve.P256,
        use=Use.SIG,
        **kwargs,
    )


__all__ = ('standard', 'es256')
