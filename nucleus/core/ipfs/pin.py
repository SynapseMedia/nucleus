from nucleus.core.types import CID

from .types import Pin, LocalPin
from .cmd import IPFS


def remote(cid: CID, service_name: str) -> Pin:
    """Pin cid into remote service.
    Service should be already registered otherwise raise IPFSFailedExecution.
    ref: http://docs.ipfs.io/reference/cli/#ipfs-pin-remote-add

    Output:
        {
            "Status": "queued",
            "Cid": "QmZ4agkfrVHjLZUZ8EZnNqxeVfNW5YpxNaNYLy1fTjnYt1",
            "Name": ""
        }


    :param cid: the cid to pin
    :param service_name: name of registered service
    :return: ipfs output for remote pin
    :rtype: Pin
    :raises IPFSRuntimeException: if cid already pinned or remote service fail
    """

    service_name = "--service=%s" % service_name
    background_mode = f"--background={True}"
    args = (cid, service_name, background_mode)

    # Exec command and get output
    call = IPFS("/pin/remote/add", args)()
    output = call.output

    return Pin(
        status=output.get("Status"),  # status: queue using background
        cid=output.get("Cid"),  # resulting cid
        name=output.get("Name"),  # named pin
    )


def local(cid: CID) -> LocalPin:
    """Pin cid into local node
    ref: http://docs.ipfs.io/reference/cli/#ipfs-pin

    Output:
        {
            "Pins":["QmZ4agkfrVHjLZUZ8EZnNqxeVfNW5YpxNaNYLy1fTjnYt1"]
        }

    :param cid: the cid to pin
    :return: ipfs output for ipfs local pin
    :rtype: LocalPin
    :raises IPFSRuntimeException: if ipfs cmd execution fail
    """
    # Exec command and get output
    call = IPFS("/pin/add/", cid)()
    return LocalPin(pins=call.output.get("Pins"))
