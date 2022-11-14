import src.core.ipfs.add as add

from src.core.types import Any

expected_hash = "QmRoo28ogKQ6ds3jk9x7X7x3sjTs2yTMu5vHUPxLN8vinU"


class MockCLI:
    cmd: str
    args: str

    def __call__(self):
        return {"output": expected_hash}


def test_add(mocker: Any):
    """Should return a valid cid for valid dir"""

    mocker.patch("src.core.ipfs.add.CLI", return_value=MockCLI())
    add_directory = add.directory("/test/dir")
    assert add_directory == expected_hash
