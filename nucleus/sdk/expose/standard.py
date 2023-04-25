import functools

from dataclasses import dataclass
from .types import Header, Payload

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




@dataclass
class SEP001:
    header: Header
    payload: Payload

    def descriptive(self, model: Meta):
        self.D = D(**model.dict())

    def structural(self, model: Object):
        return S(cid=model.hash)

    def technical(self, model: SimpleNamespace):
        ...

    def generate(self):
        ...


__all__ = ["SEP001", "Payload", "Header"]
