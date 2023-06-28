from dataclasses import dataclass

import nucleus.core.http as http_client
from nucleus.core.http import Response
from nucleus.core.types import CID, JSON, URL
from nucleus.sdk.exceptions import StorageServiceError

from .constants import ESTUARY_API_PIN, ESTUARY_API_PUBLIC
from .types import Object, Pin


@dataclass
class Estuary:
    """Estuary API service client.

    Usage:

        estuary_endpoint = "https://api.estuary.tech"
        estuary_key =  "ESTbb693fa8-d758-48ce-9843-a8acadb98a53ARY" # fake key
        estuary = EstuaryClient(estuary_endpoint, estuary_key)

        pin = estuary.pin(stored_object)
        removed_cid = estuary.unpin(pin.cid)


    """

    endpoint: URL
    key: str

    def __post_init__(self):
        self._http = http_client.live_session(self.endpoint)
        self._http.headers.update({'Authorization': f'Bearer {self.key}'})
        self._http.headers.update({'Content-Type': 'application/json'})

    def _safe_request(self, res: Response) -> JSON:
        """Amplifier helper method to handle response from Estuary API

        :param res: Expected response
        :return: Json response
        :raises StorageServiceError: If an error occurs during request
        """

        # expected response as json
        response = res.json()

        # if response fail
        if not res.ok:
            """
            Observable behavior:
                {
                    "code": 0,
                    "details": "string",
                    "reason": "string"
                }
            """

            error_description = response['error']['details']
            raise StorageServiceError(f'exception raised during request: {error_description}')

        return JSON(response)

    def _content_by_cid(self, cid: CID) -> JSON:
        """Collect details from estuary based on CID

        :param cid: Cid to retrieve content details
        :return: Cid content details
        :raises EdgePinException: If pin request fails
        """

        content_uri = f'{ESTUARY_API_PUBLIC}/by-cid/{cid}'
        req = self._http.get(content_uri)

        # expected response as json
        response = self._safe_request(req)
        return response.get('content', {})

    def pin(self, obj: Object) -> Pin:
        """Pin cid into estuary

        :param obj: Object to pin
        :return: Pin object
        :raises StorageServiceError: If pin request fails
        """

        # https://docs.estuary.tech/Reference/SwaggerUI#/pinning/post_pinning_pins
        data = str(JSON({'cid': obj.hash, 'name': obj.name, 'meta': {}, 'origins': []}))

        req = self._http.post(ESTUARY_API_PIN, data=data)
        json_response = self._safe_request(req)

        return Pin(
            cid=json_response['cid'],
            name=json_response['name'],
            status='pending',
        )

    def unpin(self, cid: CID) -> CID:
        """Remove pin from estuary

        :param cid: The cid to remove from service
        :return: The recently removed CID
        :raises StorageServiceError: if an error occurs during request
        """

        # content id is same as pin id
        pin_id = self._content_by_cid(cid).get('id')
        response = self._http.delete(f'{ESTUARY_API_PIN}/{pin_id}')
        # If error happens then raise standard exception.
        self._safe_request(response)
        return cid


__all__ = ['Estuary']
