import pytest
from typing import Any
from src.core.storage.types import Service, Services
from src.core.storage.service import service, register
from src.core.exceptions import IPFSFailedExecution

PATH_CLI_PATCH = "src.core.storage.service.CLI"


class MockFailingCLI:
    msg: str

    def __init__(self, message: str):
        self.msg = message

    def __call__(self):
        # Check for raising error for any resulting fail
        raise IPFSFailedExecution(self.msg)


def test_register_service(mocker: Any):
    """Should return a valid output for valid service registration"""

    register_service = Service(
        **{
            "service": "edge",
            "endpoint": "http://localhost",
            "key": "abc123",
        }
    )

    class MockCLI:
        cmd: str
        args: str

        def __call__(self):
            return {"output": None}

    mocker.patch(PATH_CLI_PATCH, return_value=MockCLI())
    registered_service = register(register_service)

    assert registered_service == registered_service


def test_services(mocker: Any):
    """Should return a valid output for valid service registration"""
    expected_services = [
        {
            "Service": "pinata",
            "ApiEndpoint": "https://api.pinata.cloud/psa",
        },
        {
            "Service": "pinata2",
            "ApiEndpoint": "https://api.pinata.cloud/psa",
        },
    ]

    class MockCLI:
        cmd: str
        args: str

        def __call__(self):
            return {"output": {"RemoteServices": expected_services}}

    mocker.patch(PATH_CLI_PATCH, return_value=MockCLI())
    registered_services = service()
    services_iter = map(
        lambda x: Service(service=x["Service"], endpoint=x["ApiEndpoint"], key=None),
        expected_services,
    )

    assert list(registered_services["remote"]) == list(
        Services(remote=services_iter)["remote"]
    )


def test_invalid_register_service(mocker: Any):
    """Should raise error for already registered service"""
    register_service = Service(
        service="edge",
        endpoint="http://localhost",
        key="abc123",
    )

    # Simulating an error returned by ipfs invalid service
    expected_issue = "Error: service already present"
    mocker.patch(PATH_CLI_PATCH, return_value=MockFailingCLI(expected_issue))
    with pytest.raises(IPFSFailedExecution):
        register(register_service)
