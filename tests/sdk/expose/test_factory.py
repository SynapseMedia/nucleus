import nucleus.sdk.expose as expose
from nucleus.sdk.expose import SignKeyRing


def test_ecdsa_factory():
    """Should return an expected and valid SigKeyRing"""

    ecdsa = expose.es256()

    assert isinstance(ecdsa, SignKeyRing)
    assert ecdsa.alg == 'ES256'
    assert ecdsa.crv == 'P-256'
    assert ecdsa.use == 'sig'
    assert ecdsa.kty == 'EC'
