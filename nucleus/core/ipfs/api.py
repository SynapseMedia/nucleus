import nucleus.core.exceptions as exceptions

from nucleus.core.http import LiveSession
from nucleus.core.types import JSON
from .types import RPCCommand


class IPFSApi:

    """IPFS strategically interact with different rpc command and execute them in a safe manner.
    Each http call is preset with base url and version and the complement of the url is added during runtime based on each rpc command implementation.
        eg. localhost:5001/api/v0 + /add, /config, ...

    """

    _http: LiveSession

    def __init__(self, http_client: LiveSession):
        self._http = http_client

    def __call__(self, command: RPCCommand) -> JSON:
        """Execute built command in container

        :return: json response from IPFS API call response
        :rtype: JSON
        :raises IPFSRuntimeException: if status code is not 200

        200 - The request was processed or is being processed (streaming)
        500 - RPC endpoint returned an error
        400 - Malformed RPC, argument type error, etc
        403 - RPC call forbidden
        404 - RPC endpoint doesn't exist
        405 - HTTP Method Not Allowed
        """

        # we pass an out of the box http session
        response = command(self._http)
        if not response.ok:
            raise exceptions.IPFSRuntimeError(
                f"error trying to execute IPFS command `{command.__class__.__name__}`: {response.reason}"
            )

        # ready to use response
        return response.json()


__all__ = ("IPFSApi",)
