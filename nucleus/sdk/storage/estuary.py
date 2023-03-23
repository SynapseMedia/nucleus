import nucleus.sdk.exceptions as exceptions
import nucleus.core.http as http

from dataclasses import dataclass
from nucleus.core.http import Response
from nucleus.core.types import Iterator, CID, Any, JSON, URL
from .constants import ESTUARY_API_PIN, ESTUARY_API_PUBLIC
from .types import Pin


# ESTbb693fa8-d758-48ce-9843-a8acadb98a53ARY


def _pin_factory(raw_pin: JSON):
    """Pin factory from raw pin list

    :param raw_pin: dictionary with pin information
    :return: pin object
    :rtype: Pin
    """
    pin = raw_pin.get("pin", {})
    status = raw_pin.get("status", "fail")
    # pin subfields
    # ref:
    # https://docs.estuary.tech/Reference/SwaggerUI#/pinning/get_pinning_pins
    name = pin.get("name", "estuary")
    cid = pin.get("cid", CID(""))
    return Pin(cid, status, name)


def _enhanced_response(res: Response) -> JSON:
    """Amplifier helper function to handle response from Estuary API

    :param res: expected response
    :return: json response
    :rtype: JSON
    :raises StorageServiceError: if an error occurs during request
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
        error_description = response.get("details", "")
        raise exceptions.StorageServiceError(
            f"exception raised during request: {error_description}",
        )

    return response


@dataclass
class Estuary:
    endpoint: URL
    key: str

    def __post_init__(self):
        self._http = http.live_session(self.endpoint)
        self._http.headers.update({"Authorization": f"Bearer {self.key}"})

    def _content_by_cid(self, cid: CID) -> JSON:
        """Collect details from estuary based on CID
        ref: https://docs.estuary.tech/Reference/SwaggerUI#/public/get_public_by_cid__cid_

        :param cid: cid to retrieve content details
        :return: cid content details
        :rtype: JSON
        :raises EdgePinException: if pin request fails
        """

        content_uri = f"{ESTUARY_API_PUBLIC}/by-cid/{cid}"
        req = self._http.get(content_uri)

        # expected response as json
        response = _enhanced_response(req)
        return response.get("content", {})

    def pin(self, cid: CID, **kwargs: Any) -> Pin:
        """Pin cid into remote edge cache

        :param cid: cid to pin
        :return: pin object
        :rtype: Pin
        :raises EdgePinException: if pin request fails
        """
        req = self._http.post(ESTUARY_API_PIN, data={cid: cid, **kwargs})
        response = _enhanced_response(req)
        # data resulting from estuary endpoint
        # ref: https://docs.estuary.tech/Reference/SwaggerUI#/pinning/post_pinning_pins
        return _pin_factory(response)

    def ls(self) -> Iterator[Pin]:
        """Return current remote pin list
        ref: http://docs.ipfs.io/reference/cli/#ipfs-pin-remote-ls

        :param limit: number of remote pins to return
        :return: list of current remote pin list
        :rtype: Iterator[Pin]
        :raises EdgePinException: if pin request fails
        """
        # expected response as json
        req = self._http.get(ESTUARY_API_PIN)

        # expected response as json
        response = _enhanced_response(req)
        pin_list = response.get("results", [])
        return map(_pin_factory, pin_list)

    def unpin(self, cid: CID):
        """Remove pin from edge cache service

        :param cid: cid to remove from cache
        :return: none since we don't receive anything from estuary
        :rtype: None
        :raises EdgePinException: if an error occurs during request
        """

        pin_id = self._content_by_cid(cid).get("id")  # content id is same as pin id
        req = self._http.delete(f"{ESTUARY_API_PIN}/{pin_id}")
        # we don't consume anything since delete is empty response
        _enhanced_response(req)
