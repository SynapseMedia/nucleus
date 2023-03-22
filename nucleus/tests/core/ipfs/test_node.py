import nucleus.core.ipfs.node as node

from nucleus.core.ipfs.constants import EXIT_SUCCESS
from nucleus.core.types import Any, StdOut


def test_node_id(mocker: Any):
    """Should return a valid ipfs id"""

    class MockCLI:
        cmd: str
        args: str

        def __call__(self):
            return StdOut(EXIT_SUCCESS,
                          {"ID": "12D3KooWAsERf3AYJZ8XkGPK4svfEzoy3x8uM16H6PKzamNkppgp",
                           "PublicKey": "CAESIA+XrKfYJJNF0iru64PmL2i/tO3EESGnxUGOrDnD+bJJ",
                           "Addresses": [...],
                              "AgentVersion": "go-ipfs/0.10.0/64b532f",
                              "ProtocolVersion": "ipfs/0.1.0",
                              "Protocols": [...],
                           },
                          )

    mocker.patch("src.core.ipfs.node.IPFS", return_value=MockCLI())
    assert node.id() == "12D3KooWAsERf3AYJZ8XkGPK4svfEzoy3x8uM16H6PKzamNkppgp"
