import pytest
import src.core.ipfs.dag as dag

from src.core.ipfs.types import Result
from src.core.types import Any, CID


def test_dag_get(mocker: Any):
    """Should return a valid dag for valid cid"""

    expected_dag = {
        "Data": {"/": {"bytes": "CAIY1qEQIICAECDWIQ"}},
        "Links": [
            {
                "Hash": {"/": "QmRoo28ogKQ6ds3jk9x7X7x3sjTs2yTMu5vHUPxLN8vinU"},
                "Name": "",
                "Tsize": 262158,
            },
        ],
    }

    class MockCLI:
        cmd: str
        args: str

        def __call__(self):
            return Result(expected_dag)

    mocker.patch("src.core.ipfs.dag.CLI", return_value=MockCLI())
    dag_get = dag.get(CID("QmZ4agkfrVHjLZUZ8EZnNqxeVfNW5YpxNaNYLy1fTjnYt1"))
    assert dag_get.data == expected_dag.get("Data")

    for i, link in enumerate(dag_get.links):
        expected_links = expected_dag["Links"]
        expected_link = expected_links[i]  # type: ignore

        assert link.name == expected_link["Name"]
        assert link.hash == expected_link.get("Hash")
        assert link.tsize == expected_link.get("Tsize")


def test_invalid_dag_get(mocker: Any):
    """Should raise error for invalid dag get cid"""

    class MockFailingCLI:
        msg: str

        def __init__(self, message: str):
            self.msg = message

        def __call__(self):
            # Check for raising error for any resulting fail
            raise RuntimeError(self.msg)

    duplicated_cid = "abcde"
    # Simulating an error returned by ipfs invalid cid
    expected_issue = 'Error: invalid path "QmZ4agkfrVHjLZUZ8EZnNqxeVfNW5YpxNaNYLy1fTjnYt": selected encoding not supported'
    mocker.patch("src.core.ipfs.dag.CLI", return_value=MockFailingCLI(expected_issue))
    with pytest.raises(RuntimeError):
        dag.get(CID(duplicated_cid))
