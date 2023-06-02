from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from nucleus.core.types import Raw, Setting

from .types import JWK

"""
We can support more
ref: https://www.rfc-editor.org/rfc/rfc7518#section-3.1
ref: https://datatracker.ietf.org/doc/html/rfc7517#section-4.1
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


class Use(str, Enum):
    SIG = 'sig'
    ENC = 'enc'


class KeyType(str, Enum):
    RSA = 'RSA'
    EllipticCurve = 'EC'


class Curve(str, Enum):
    HMAC = 'HMAC'
    P256 = 'P-256'
    ED25519 = 'ED25519'
    Secp256k1 = 'secp256k1'


class Algorithm(str, Enum):
    H256 = 'H256'
    ES256 = 'ES256'
    ES256K = 'ES256K'


# class EncKeyRing:
#     ...


@dataclass(slots=True)
class SignKeyRing:
    alg: Algorithm
    key_type: KeyType
    curve: Curve
    use: Use

    # internal jwk interface
    _jwk: JWK = field(init=False)
    # filter included members in jwk object
    __allowed__ = (
        'crv',
        'kty',
        'x',
        'y',
    )

    def __iter__(self) -> Setting:
        """Export extra headers to add into serialization"""
        jwk: Raw = {k: v for k, v in self._jwk.items() if k in self.__allowed__}  # type: ignore
        yield 'alg', self.alg.value
        yield 'jwk', jwk

    def __post_init__(self):
        # Initialize _jwk as new JWK object
        # ref: https://jwcrypto.readthedocs.io/en/latest/jwk.html
        self.jwk = JWK.generate(  # type: ignore
            alg=self.alg.value,
            kty=self.key_type.value,
            curve=self.curve.value,
            use=self.use.value,
        )


__all__ = ('SignKeyRing', 'Algorithm', 'Curve', 'KeyType', 'Use')
