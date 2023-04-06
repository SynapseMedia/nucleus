import pytest
import responses
import nucleus.sdk.storage as storage
import nucleus.sdk.exceptions as exceptions

from nucleus.core.types import CID
from nucleus.sdk.storage import Estuary, Pin


@responses.activate
def test_estuary_pin(mock_estuary_service: Estuary, mock_estuary_pin_cid_request: CID):
    """Should return valid Pin for valid CID"""
    estuary = storage.service(mock_estuary_service)
    pinned = estuary.pin(mock_estuary_pin_cid_request)

    assert pinned == Pin(
        cid=mock_estuary_pin_cid_request,
        status="pending",
        name="estuary",
    )


def test_estuary_ob(mock_estuary_service: Estuary, mock_cid: CID):
    """Should fail on purpose to track the observable error behavior from Estuary"""
    estuary = storage.service(mock_estuary_service)
    with pytest.raises(exceptions.StorageServiceError):
        estuary.pin(mock_cid)


@responses.activate
def test_estuary_fail_request(
    mock_estuary_service: Estuary, mock_estuary_invalid_request: CID
):
    """Should raise an exception if the cid is not valid neither exists"""
    with pytest.raises(exceptions.StorageServiceError):
        estuary = storage.service(mock_estuary_service)
        estuary.unpin(mock_estuary_invalid_request)
