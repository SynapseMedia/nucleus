from nucleus.core.types import Any

from .key import Algorithm, Curve, KeyType, SignKeyRing, Use
from .sep import SEP001, Header, Payload


def standard(type: str) -> SEP001:
    """SEP-001 factory function.

    Usage:

        # create a new sep-001-video/mp4 instance
        media_type = "video/mp4"
        sep001 = expose.standard(media_type)

    :param type: The type of media to expose
    :return: New standard implementation sep-001 object
    """

    return SEP001(
        Header(type),
        Payload(),
    )


def es256(**kwargs: Any) -> SignKeyRing:
    """Return a KeyRing with ECDSA settings based on JWA RFC7518 spec.

    Usage:

        # create a KeyRing with ECDSA settings
        sign_algorithm = expose.es256()

    :param **kwargs: Any extra settings could be passed as keyword arguments
    :return: Ready to use ecdsa signature keyring
    """

    return SignKeyRing(
        alg=Algorithm.ES256,
        key_type=KeyType.EllipticCurve,
        curve=Curve.P256,
        use=Use.SIG,
        **kwargs,
    )


__all__ = ('standard', 'es256')
