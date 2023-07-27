import nucleus.sdk.expose as expose
from nucleus.core.types import Raw
from nucleus.sdk.expose import SignKeyRing


def test_key_fingerprint(mock_jwk: Raw):
    """Should return expected sha256 fingerprint from JWK dict"""
    expected_hash = 'e7aa40f080fe6eeda99a5b97934044355769e5eaedad06a605e2424f92b7bb44'
    ecdsa = SignKeyRing.from_dict(mock_jwk)
    assert expected_hash == ecdsa.fingerprint()


def test_key_export():
    """Should export the expected fingerprint for exported key"""
    # export the initialized key
    sign_key = expose.es256()
    exported_jwk = sign_key.as_dict()
    expected_hash = sign_key.fingerprint()

    # re-import the key to validate fingerprint
    restored_key = SignKeyRing.from_dict(exported_jwk)
    assert expected_hash == restored_key.fingerprint()
