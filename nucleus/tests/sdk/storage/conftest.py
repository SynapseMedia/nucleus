import pytest
import responses
import json

from nucleus.core.types import CID
from nucleus.sdk.storage import EstuarySvc

ENDPOINT = "https://api.estuary.tech"

expected_cid = CID("bafyjvzacdi2ry54h6wd7muu2wyy3x74xia2wldqnlxpgyg44z2uq")
expected = {
    "results": [
        {
            "status": "pinned",
            "pin": {
                "cid": expected_cid,
                "name": "estuary",
            },
        }
    ],
}


@pytest.fixture()
def mock_estuary_service():
    return EstuarySvc(
        key="abcd12345",
    )


@pytest.fixture()
def mock_pinned_cid_request():

    # expected response from estuary API
    responses.add(
        method=responses.GET,
        url=f"{ENDPOINT}/pinning/pins",
        body=json.dumps(expected),
        status=200,
        content_type="application/json",
        stream=True,
    )

    return expected_cid


@pytest.fixture()
def mock_invalid_request():
    # expected response from estuary API
    responses.add(
        method=responses.GET,
        url=f"{ENDPOINT}/pinning/pins",
        status=500,
        stream=True,
    )

    return CID("invalid_cid")
