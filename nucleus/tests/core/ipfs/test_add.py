import nucleus.core.ipfs.add as add

from nucleus.core.ipfs.constants import EXIT_SUCCESS
from nucleus.core.types import Any, Path, StdOut


expected_hash = "QmRoo28ogKQ6ds3jk9x7X7x3sjTs2yTMu5vHUPxLN8vinU"


class MockCLI:
    cmd: str
    args: str

    def __call__(self):
        return StdOut(EXIT_SUCCESS, expected_hash)


def test_add(mocker: Any):
    """Should return a valid cid for valid dir"""

    mocker.patch("nucleus.core.ipfs.add.IPFS", return_value=MockCLI())
    add_directory = add.directory(Path("/test/dir"))
    assert add_directory == expected_hash
