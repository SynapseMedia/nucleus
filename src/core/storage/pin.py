from src.core.types import CIDStr

from .types import RemotePin, LocalPin, Service
from .ipfs import CLI


def remote(cid: CIDStr, service: Service, background: bool = True) -> RemotePin:
    """Pin cid into edge pinata remote cache
    ref: http://docs.ipfs.io/reference/cli/#ipfs-pin-remote-add

    Output:
        {
            "Status": "queued",
            "Cid": "QmZ4agkfrVHjLZUZ8EZnNqxeVfNW5YpxNaNYLy1fTjnYt1",
            "Name": ""
        }


    :param cid: the cid to pin
    :param service: Service settings
    :param background: Run pin process in background mode
    :return: ipfs output for remote pin
    :rtype: RemotePin
    :raises IPFSFailedExecution
    """

    service_name = "--service=%s" % service["service"]
    background_mode = f"--background={background}"
    args = (cid, service_name, background_mode)

    # Exec command and get output
    exec = CLI("/pin/remote/add", args)
    output = exec().get("output")

    return RemotePin(
        status=output.get("Status"),  # status: queue using background
        cid=output.get("Cid"),  # resulting cid
        name=output.get("Name"),  # named pin
    )


def local(cid: CIDStr) -> LocalPin:
    """Pin cid into local node
    ref: http://docs.ipfs.io/reference/cli/#ipfs-pin

    Output:
        {
            "Pins":["QmZ4agkfrVHjLZUZ8EZnNqxeVfNW5YpxNaNYLy1fTjnYt1"]
        }

    :param cid: the cid to pin
    :return: ipfs output for ipfs local pin
    :rtype: LocalPin
    :raises IPFSFailedExecution
    """
    # Exec command and get output
    exec = CLI("/pin/add/", cid)
    output = exec().get("output")
    return LocalPin(pins=output.get("Pins"))
