from dataclasses import dataclass
from nucleus.core.types import CID

"""Standard implementation for SEP-001 extends JWT standard.
ref: https://www.rfc-editor.org/rfc/rfc7519
ref: https://www.iana.org/assignments/jwt/jwt.xhtml
Validation:
1) valid JWT?
2) hash valid SEP001 standard?
    - has s and d fields
    - s and d has expected Meta, Media schema?

"""


"""
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


@dataclass(slots=True)
class Header:
    typ: str  # Is used by JWT applications to declare the media type [IANA.MediaTypes] of this complete JWT
    alg: str = "HS256"  # The "alg" (algorithm) Header Parameter identifies the cryptographic algorithm used in signature creation


@dataclass(slots=True)
class Payload:
    iat: int  # The "iat" (issued at) claim identifies the time at which the JWT was issued.
    iss: str  # The "iss" (issuer) claim identifies the principal that issued the JWT.
    s: CID  # s: structural metadata CID (meta for media resources)
    d: CID  # d: descriptive metadata CID


@dataclass(slots=True)
class SEP001:
    header: CID
    payload: CID


__all__ = ["SEP001", "Payload", "Header"]
