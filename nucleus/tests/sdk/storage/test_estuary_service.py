import responses
import pytest
import nucleus.sdk.storage as storage
import nucleus.sdk.exceptions as exceptions

from nucleus.core.ipfs import Service, Pin
from nucleus.core.types import CID


def test_estuary_uri_builder(mock_estuary_service: Service):
    """Should return expected uri based on service endpoint"""
    estuary = storage.Estuary(mock_estuary_service)
    uri = estuary._build_uri("/demo/path")  # type: ignore
    assert uri == f"{mock_estuary_service.endpoint}/demo/path"


@responses.activate
def test_ls_pinned_cid(
        mock_pinned_cid_request: CID,
        mock_estuary_service: Service):
    """Should fetch a list of Pins stored in estuary"""

    estuary = storage.Estuary(mock_estuary_service)
    got = list(estuary.ls())

    # expected a list of pins
    expected = [Pin(status="pinned",
                    cid=mock_pinned_cid_request,
                    name="estuary")]
    assert got == expected


def test_estuary_fail_request(
        mock_estuary_service: Service,
        mock_invalid_request: CID):

    with pytest.raises(exceptions.StorageServiceError):
        estuary = storage.Estuary(mock_estuary_service)
        estuary.unpin(mock_invalid_request)
