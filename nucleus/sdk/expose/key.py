from __future__ import annotations

from dataclasses import KW_ONLY, dataclass, field
from enum import Enum

from jwcrypto.common import base64url_decode

from nucleus.core.types import JSON, Raw, Setting

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


@dataclass(slots=True)
class SignKeyRing:
    alg: Algorithm
    key_type: KeyType
    curve: Curve
    use: Use

    _: KW_ONLY
    # avoid to auto-gen the JWK
    lazy_mode: bool = False
    # internal jwk interface
    _jwk: JWK = field(init=False)

    def __iter__(self) -> Setting:
        """Yield `alg` and `jwk` headers specified in RFC 7517-7516 standard.

        :return: The iterable header settings to associate
        """
        yield 'alg', self.alg.value
        yield 'jwk', self._jwk.export_public(True)

    def __post_init__(self):
        # Initialize jwk as new JWK object
        # ref: https://jwcrypto.readthedocs.io/en/latest/jwk.html
        if self.lazy_mode:
            return

        self._jwk = JWK.generate(
            alg=self.alg.value,
            kty=self.key_type.value,
            curve=self.curve.value,
            use=self.use.value,
        )

    def jwk(self) -> JWK:
        """Return the internal JWK (JSON Web Key) instance

        :return: The JWK (JSON Web Key) instance
        """
        return self._jwk

    def as_dict(self) -> Raw:
        """Export Keyring as JWK JSON format

        :return: Keyring as dict
        """
        return self._jwk.export(True, True)  # type: ignore

    def from_dict(self, raw_key: Raw) -> SignKeyRing:
        """Initialize Keyring using JWK JSON format

        :param raw_key: Keyring to import as dict (JSON format)
        :return: KeyRing object
        """
        json_string = str(JSON(raw_key))
        self._jwk = JWK.from_json(json_string)
        return self

    def fingerprint(self) -> str:
        """Return the base64 decoded thumbprint as specified by RFC 7638.

        :return: The decoded sha256 thumbprint.
        """
        b64_thumbprint = self._jwk.thumbprint()
        decoded_thumbprint = base64url_decode(b64_thumbprint)
        return decoded_thumbprint.hex()


__all__ = ('SignKeyRing', 'Algorithm', 'Curve', 'KeyType', 'Use')
