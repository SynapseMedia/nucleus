import json

from requests.exceptions import JSONDecodeError

from nucleus.core.exceptions import IPFSRuntimeError
from nucleus.core.http import LiveSession
from nucleus.core.types import JSON

from .types import RPCCommand


class RPC:

    """IPFS strategically interact with different rpc command and execute them in a safe manner.
    Each http call is preset with base url and version and the complement of the url is added during runtime
    based on each rpc command implementation.
        eg. localhost:5001/api/v0 + /add, /config, ...

    """

    _http: LiveSession

    def __init__(self, http_client: LiveSession):
        self._http = http_client

    def __call__(self, command: RPCCommand) -> JSON:
        """Execute built command in container

        :return: json response from IPFS API call response
        :raises IPFSRuntimeException: If status code is not 200

        200 - The request was processed or is being processed (streaming)
        500 - RPC endpoint returned an error
        400 - Malformed RPC, argument type error, etc
        403 - RPC call forbidden
        404 - RPC endpoint doesn't exist
        405 - HTTP Method Not Allowed
        """

        # we pass an out of the box http session
        response = command(self._http)

        try:
            json_response = response.json()
        except JSONDecodeError:
            # sometime the IPFS output is not JSON
            byte_content = response.content
            string_content = byte_content.decode('utf-8')

            # we expect this behavior when a directory is added
            # IPFS output in this case is a list of json separated by \n
            matched_delimiter = string_content.split('\n')
            if len(matched_delimiter) == 0:
                raise

            json_dicts = map(json.loads, filter(None, matched_delimiter))
            sorted_sizes = sorted(json_dicts, key=lambda d: int(d['Size']), reverse=True)
            return JSON(sorted_sizes[0])

        # check if request was successful
        if not response.ok:
            error_details = json_response.get('Message')
            raise IPFSRuntimeError(f'error trying to execute IPFS command `{type(command).__name__}`: {error_details}')

        # ready to use response
        return json_response


__all__ = ('RPC',)
