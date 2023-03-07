import src.core.ipfs.add as add

from src.core.ipfs.constants import EXIT_SUCCESS
from src.core.types import Any, Path, StdOut


expected_hash = "QmRoo28ogKQ6ds3jk9x7X7x3sjTs2yTMu5vHUPxLN8vinU"


class MockCLI:
    cmd: str
    args: str

    def __call__(self):
        return StdOut(EXIT_SUCCESS, expected_hash)


def test_add(mocker: Any):
    """Should return a valid cid for valid dir"""

    mocker.patch("src.core.ipfs.add.CLI", return_value=MockCLI())
    add_directory = add.directory(Path("/test/dir"))
    assert add_directory == expected_hash
