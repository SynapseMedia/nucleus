import pytest

import nucleus.sdk.expose as expose


@pytest.fixture()
def mock_jwk():
    return {
        'kty': 'EC',
        'use': 'sig',
        'alg': 'ES256',
        'crv': 'P-256',
        'x': 'aPte1VlVvfw8hZxd6sge-9B38_DrdcDufTfRpNHBGlA',
        'y': 'VM_piv4WGEzTBdcWRKmDoG4VAdTC806GXMjRKWOq0Ww',
    }


@pytest.fixture()
def mock_sign_keyring(mock_jwk):
    # avoid to auto-init keyring
    ecdsa = expose.es256(lazy_mode=True)
    return ecdsa.from_dict(mock_jwk)
