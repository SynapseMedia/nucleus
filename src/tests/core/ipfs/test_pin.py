import pytest
import src.core.ipfs.pin as pin
import src.core.exceptions as exceptions

from src.core.ipfs.types import LocalPin, RemotePin, Result
from src.core.types import Any, CID


class MockFailingCLI:
    msg: str

    def __init__(self, message: str):
        self.msg = message

    def __call__(self):
        # Check for raising error for any resulting fail
        raise exceptions.IPFSFailedExecution(self.msg)


def test_pin_local(mocker: Any):
    """Should return a valid output for valid pin"""

    expected_pins = ["QmZ4agkfrVHjLZUZ8EZnNqxeVfNW5YpxNaNYLy1fTjnYt1"]

    class MockCLI:
        cmd: str
        args: str

        def __call__(self):
            return Result({"Pins": expected_pins})

    mocker.patch("src.core.ipfs.pin.CLI", return_value=MockCLI())
    pins = pin.local(CID("QmZ4agkfrVHjLZUZ8EZnNqxeVfNW5YpxNaNYLy1fTjnYt1"))

    assert pins.get("pins") == expected_pins
    assert pins == LocalPin(pins=expected_pins)


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
            return Result(expected_result)

    mocker.patch("src.core.ipfs.pin.CLI", return_value=MockCLI())
    cid_to_pin = "QmZ4agkfrVHjLZUZ8EZnNqxeVfNW5YpxNaNYLy1fTjnYt1"
    pins = pin.remote(CID(cid_to_pin), "edge")

    assert expected_result["Status"] == pins["status"]
    assert expected_result["Cid"] == pins["cid"]
    assert expected_result["Name"] == pins["name"]
    assert pins == RemotePin(
        status=expected_result["Status"],
        cid=expected_result["Cid"],
        name=expected_result["Name"],
    )


def test_invalid_pin_remote(mocker: Any):
    """Should raise error for invalid pin"""
    invalid_cid = "abcde"
    # Simulating an error returned by ipfs invalid cid
    expected_issue = 'Error: invalid path "abcde": selected encoding not supported'
    mocker.patch("src.core.ipfs.pin.CLI", return_value=MockFailingCLI(expected_issue))
    with pytest.raises(exceptions.IPFSFailedExecution):
        pin.local(CID(invalid_cid))


def test_invalid_pin_local(mocker: Any):
    """Should raise error for invalid remote pin"""
    duplicated_cid = "abcde"
    # Simulating an error returned by ipfs invalid cid
    expected_issue = 'Error: reason: "DUPLICATE_OBJECT", details: "Object already pinned to pinata. Please remove or replace existing pin object."'
    mocker.patch("src.core.ipfs.pin.CLI", return_value=MockFailingCLI(expected_issue))
    with pytest.raises(exceptions.IPFSFailedExecution):
        pin.remote(CID(duplicated_cid), "edge")
