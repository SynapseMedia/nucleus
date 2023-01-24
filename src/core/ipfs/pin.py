from src.core.types import CID

from .types import RemotePin, LocalPin
from .cmd import CLI


def remote(cid: CID, service: str) -> RemotePin:
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
    :param service: name of registered service
    :return: ipfs output for remote pin
    :rtype: RemotePin
    :raises IPFSFailedExecution: if cid already pinned or remote service fail
    """

    service = "--service=%s" % service
    background_mode = f"--background={True}"
    args = (cid, service, background_mode)

    # Exec command and get output
    call = CLI("/pin/remote/add", args)()
    output = call.output

    return RemotePin(
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
    :raises IPFSFailedExecution: if ipfs cmd execution fail
    """
    # Exec command and get output
    call = CLI("/pin/add/", cid)()
    return LocalPin(pins=call.output.get("Pins"))
