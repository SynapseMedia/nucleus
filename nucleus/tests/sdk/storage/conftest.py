import pytest
import responses
import json

from nucleus.core.types import CID, URL
from nucleus.sdk.storage import Estuary

ENDPOINT = "https://api.estuary.tech"

expected_cid = CID("bafyjvzacdi2ry54h6wd7muu2wyy3x74xia2wldqnlxpgyg44z2uq")
expected_error = {"error": {"code": 0, "details": "string", "reason": "string"}}
expected = {
    "cid": expected_cid,
    "name": "estuary",
}


@pytest.fixture()
def mock_estuary_service():
    return Estuary(URL(ENDPOINT), "test")

@pytest.fixture()
def mock_cid():
    return expected_cid


@pytest.fixture()
def mock_estuary_pin_cid_request():

    # expected response from estuary API
    responses.add(
        method=responses.POST,
        url=f"{ENDPOINT}/pinning/pins",
        body=json.dumps(expected),
        status=200,
        content_type="application/json",
        stream=True,
    )

    return expected_cid


@pytest.fixture()
def mock_estuary_invalid_request():
    # expected response from estuary API

    responses.add(
        method=responses.GET,
        url=f"{ENDPOINT}/public/by-cid/invalid_cid",
        body=json.dumps(expected_error),
        status=500,
        stream=True,
    )

    responses.add(
        method=responses.DELETE,
        url=f"{ENDPOINT}/pinning/pins",
        body=json.dumps(expected_error),
        status=500,
        stream=True,
    )

    return CID("invalid_cid")
