import nucleus.sdk.expose as expose
from nucleus.core.types import Raw
from nucleus.sdk.expose import SignKeyRing


def test_key_fingerprint(mock_jwk: Raw):
    """Should return expected sha256 fingerprint from JWK dict"""
    expected_hash = 'e7aa40f080fe6eeda99a5b97934044355769e5eaedad06a605e2424f92b7bb44'
    ecdsa = expose.es256()
    ecdsa.from_dict(mock_jwk)
    assert expected_hash == ecdsa.fingerprint()


def test_key_export(mock_sign_keyring: SignKeyRing):
    """Should export the expected fingerprint for exported key"""
    expected_hash = 'e7aa40f080fe6eeda99a5b97934044355769e5eaedad06a605e2424f92b7bb44'
    # export the initialized key
    exported_jwk = mock_sign_keyring.as_dict()
    # re-import the key to validate fingerprint
    mock_sign_keyring.from_dict(exported_jwk)
    assert expected_hash == mock_sign_keyring.fingerprint()
