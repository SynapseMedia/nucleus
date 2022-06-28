from typing import Any
from src.core.storage.node import id


def test_node_id(mocker: Any):
    """Should return a valid ipfs id"""

    class MockCLI:
        cmd: str
        args: str

        def __call__(self):
            return {
                "output": {
                    "ID": "12D3KooWAsERf3AYJZ8XkGPK4svfEzoy3x8uM16H6PKzamNkppgp",
                    "PublicKey": "CAESIA+XrKfYJJNF0iru64PmL2i/tO3EESGnxUGOrDnD+bJJ",
                    "Addresses": [...],
                    "AgentVersion": "go-ipfs/0.10.0/64b532f",
                    "ProtocolVersion": "ipfs/0.1.0",
                    "Protocols": [...],
                }
            }

    mocker.patch("src.core.storage.node.CLI", return_value=MockCLI())
    assert id() == "12D3KooWAsERf3AYJZ8XkGPK4svfEzoy3x8uM16H6PKzamNkppgp"
