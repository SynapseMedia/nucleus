import responses
import pytest
import src.sdk.media
from src.sdk.web3.storage import check_status, has_valid_registered_service

PINATA_SERVICE = "pinata"
PINATA_ENDPOINT = "https://api.pinata.cloud"


@pytest.fixture(autouse=True)
def _setup_pinata_response_ok():
    responses.add(
        responses.GET,
        f"{PINATA_ENDPOINT}/data/testAuthentication",
        json={"test": "all good"},
    )


@responses.activate
def test_check_status(mocker):
    """Should return valid status if service connected and has local registered service"""
    mocker.patch("src.sdk.web3.storage.has_valid_registered_service", return_value=True)
    assert check_status()


@responses.activate
def test_check_invalid_status(mocker):
    """Should return fail status if not service connected or has local registered service"""

    mocker.patch(
        "src.sdk.web3.storage.has_valid_registered_service", return_value=False
    )
    assert not check_status()


def test_has_valid_registered_service(mocker):
    """Should return valid True when has local `PINATA_SERVICE` registered service"""

    # generic mocking client
    class Client:
        def get_client(self):
            return self

        def request(self, *args, **kwargs):
            return [{"RemoteServices": [{"Service": "pinata"}]}]

    src.sdk.media.ingest.ipfs = Client()
    assert has_valid_registered_service()


def test_has_ivalid_registered_service(mocker):
    """Should return False when has not local `PINATA_SERVICE` registered service"""

    # generic mocking client
    class Client:
        def get_client(self):
            return self

        def request(self, *args, **kwargs):
            return [{"RemoteServices": []}]

    src.sdk.media.ingest.ipfs = Client()
    assert not has_valid_registered_service()
