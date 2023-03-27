from abc import ABCMeta
from nucleus.core.http import LiveSession, Response
from nucleus.core.types import Protocol


class RPCCommand(Protocol, metaclass=ABCMeta):
    """RPCCommand abstraction define a callable abstraction to communicate with IPFS API.
    Determinate how each command should be handled.
    Use this class to create IPFS RCP commands subtypes.
    ref: https://docs.ipfs.tech/reference/kubo/rpc/

    """

    def __call__(self, session: LiveSession) -> Response:
        ...
