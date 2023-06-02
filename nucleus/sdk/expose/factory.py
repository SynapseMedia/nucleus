from .key import Algorithm, Curve, KeyType, SignKeyRing, Use
from .sep import SEP001, Header, Payload


def standard(type: str) -> SEP001:
    """SEP001 factory

    :param type: the type of media to expose
    :return: new standard implementation sep-001 object
    :rtype: SEP001
    """

    return SEP001(
        Header(type),
        Payload(),
    )


def es256() -> SignKeyRing:
    """Return a KeyRing with ECDSA settings based on JWA specification.
    ref: https://www.rfc-editor.org/rfc/rfc7518#section-3.1
    """

    return SignKeyRing(
        alg=Algorithm.ES256,
        key_type=KeyType.EllipticCurve,
        curve=Curve.P256,
        use=Use.SIG,
    )


__all__ = ('standard', 'es256')
