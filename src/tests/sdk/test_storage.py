import responses
import pytest
from src.sdk.storage.edge import check_status, has_valid_registered_service
from src.core.constants import PINATA_ENDPOINT


@pytest.fixture(autouse=True)
def _setup_pinata_response_ok(mocker):
    responses.add(
        responses.GET,
        f"{PINATA_ENDPOINT}/data/testAuthentication",
        json={"test": "all good"},
    )


@responses.activate
def test_check_status(mocker):
    """Should return valid status if service connected and has local registered service"""
    mocker.patch("src.sdk.storage.edge.has_valid_registered_service", return_value=True)
    assert check_status()


@responses.activate
def test_check_invalid_status(mocker):
    """Should return fail status if not service connected or has local registered service"""
    mocker.patch(
        "src.sdk.storage.edge.has_valid_registered_service", return_value=False
    )
    assert not check_status()


def test_has_valid_registered_service(mocker):
    """Should return valid True when has local `PINATA_SERVICE` registered service"""
    mocker.patch(
        "src.sdk.storage.edge.services",
        return_value=[{"Service": "pinata"}],
    )
    assert has_valid_registered_service("pinata")


def test_has_invalid_registered_service(mocker):
    """Should return False when has not local `PINATA_SERVICE` registered service"""
    mocker.patch("src.sdk.storage.edge.services", return_value=[])
    assert not has_valid_registered_service("invalid")
