import pytest
from typing import Any
from src.core.storage.add import directory

expected_hash = "QmRoo28ogKQ6ds3jk9x7X7x3sjTs2yTMu5vHUPxLN8vinU"


class MockCLI:
    cmd: str
    args: str

    def __call__(self):
        return {"output": expected_hash}


def test_add(mocker: Any):
    """Should return a valid cid for valid dir"""

    mocker.patch("src.core.storage.add.CLI", return_value=MockCLI())
    mocker.patch("src.core.storage.add.resolve_root_for", return_value=("/test/dir", True))
    add_directory = directory("/test/dir")
    assert add_directory == expected_hash


def test_invalid_add(mocker: Any):
    """Should raise error for invalid directory"""
    mocker.patch("src.core.storage.add.CLI", return_value=MockCLI())
    mocker.patch("src.core.storage.add.resolve_root_for", return_value=(None, False))
    with pytest.raises(FileNotFoundError):
        directory("/not/exist/dir")
