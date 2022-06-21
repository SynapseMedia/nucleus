import pytest
from typing import Any
from src.core.storage.pin import local, remote, PinLocal, PinRemote
from src.core.exceptions import IPFSFailedExecution


class MockFailingCLI:
    msg: str

    def __init__(self, message: str):
        self.msg = message

    def __call__(self):
        # Check for raising error for any resulting fail
        raise IPFSFailedExecution(self.msg)


def test_pin_local(mocker: Any):
    """Should return a valid output for valid pin"""

    expected_pins = ["QmZ4agkfrVHjLZUZ8EZnNqxeVfNW5YpxNaNYLy1fTjnYt1"]

    class MockCLI:
        cmd: str
        args: str

        def __call__(self):
            return {"result": {"Pins": expected_pins}}

    mocker.patch("src.core.storage.pin.CLI", return_value=MockCLI())
    pins = local("QmZ4agkfrVHjLZUZ8EZnNqxeVfNW5YpxNaNYLy1fTjnYt1")
    assert pins == PinLocal(pins=expected_pins)


def test_pin_remote(mocker: Any):
    """Should return a valid output for valid remote pin"""
    expected_result = {
        "Status": "queued",
        "Cid": "QmZ4agkfrVHjLZUZ8EZnNqxeVfNW5YpxNaNYLy1fTjnYt1",
        "Name": "",
    }

    class MockCLI:
        cmd: str
        args: str

        def __call__(self):
            return {"result": expected_result}

    mocker.patch("src.core.storage.pin.CLI", return_value=MockCLI())
    pins = remote("QmZ4agkfrVHjLZUZ8EZnNqxeVfNW5YpxNaNYLy1fTjnYt1", "pinata", True)
    assert pins == PinRemote(
        status=expected_result["Status"],
        cid=expected_result["Cid"],
        name=expected_result["Name"],
    )


def test_invalid_pin_remote(mocker: Any):
    """Should raise error for invalid pin"""
    invalid_cid = "abcde"
    # Simulating an error returned by ipfs invalid cid
    expected_issue = 'Error: invalid path "abcde": selected encoding not supported'
    mocker.patch(
        "src.core.storage.pin.CLI", return_value=MockFailingCLI(expected_issue)
    )
    with pytest.raises(IPFSFailedExecution):
        local(invalid_cid)


def test_invalid_pin_local(mocker: Any):
    """Should raise error for invalid remote pin"""
    duplicated_cid = "abcde"
    # Simulating an error returned by ipfs invalid cid
    expected_issue = 'Error: reason: "DUPLICATE_OBJECT", details: "Object already pinned to pinata. Please remove or replace existing pin object."'
    mocker.patch(
        "src.core.storage.pin.CLI", return_value=MockFailingCLI(expected_issue)
    )
    with pytest.raises(IPFSFailedExecution):
        remote(duplicated_cid, "pinata", True)
