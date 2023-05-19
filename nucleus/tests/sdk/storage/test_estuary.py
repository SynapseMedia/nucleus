import pytest
import responses

import nucleus.sdk.exceptions as exceptions
import nucleus.sdk.storage as store
from nucleus.sdk.storage import Estuary, Object, Pin


@responses.activate
def test_estuary_pin(mock_estuary_service: Estuary, mock_estuary_pin_cid_request: Object):
    """Should return valid Pin for valid CID"""
    estuary = store.client(mock_estuary_service)
    pinned = estuary.pin(mock_estuary_pin_cid_request)

    assert pinned == Pin(
        cid=mock_estuary_pin_cid_request.hash,
        status='pending',
        name='estuary',
    )


def test_estuary_ob(mock_estuary_service: Estuary, mock_object: Object):
    """Should fail on purpose to track the observable error behavior from Estuary"""
    estuary = store.client(mock_estuary_service)
    with pytest.raises(exceptions.StorageServiceError):
        estuary.pin(mock_object)


@responses.activate
def test_estuary_fail_request(mock_estuary_service: Estuary, mock_estuary_invalid_request: Object):
    """Should raise an exception if the cid is not valid neither exists"""
    with pytest.raises(exceptions.StorageServiceError):
        estuary = store.client(mock_estuary_service)
        estuary.unpin(mock_estuary_invalid_request)
