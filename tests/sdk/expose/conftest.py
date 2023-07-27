import pytest


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
