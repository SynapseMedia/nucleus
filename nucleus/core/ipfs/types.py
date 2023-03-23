from nucleus.core.http import LiveSession, Response
from nucleus.core.types import Protocol, Setting


class RPCCommand(Setting, Protocol):
    """RPCCommand abstraction define a callable abstraction to communicate with IPFS API.
    Determinate how each command should be handled.
    Use this class to create IPFS RCP commands subtypes.
    ref: https://docs.ipfs.tech/reference/kubo/rpc/

    """

    def __call__(self, session: LiveSession) -> Response:
        ...
