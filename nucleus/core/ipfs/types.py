from nucleus.core.http import LiveSession, Response
from nucleus.core.types import Protocol


class RPCCommand(Protocol):
    """RPCCommand abstraction define a callable abstraction to communicate with IPFS API.
    Determinate how each command should be handled.
    Use this class to create IPFS RCP commands subtypes.
    ref: https://docs.ipfs.tech/reference/kubo/rpc/

    """

    def __call__(self, session: LiveSession) -> Response:
        """This method is called in API handler as a nested call
        ref: http://docs.ipfs.tech/reference/kubo/cli/#ipfs-add

        :param session: http "out of the box" interface
        :return: endpoint command call response
        :rtype: Response
        """
        ...
