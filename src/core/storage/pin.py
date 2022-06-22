from ..types import CIDStr
from . import CLI, Edge, Pin, Service


def remote(cid: CIDStr, service: Service, background: bool) -> Edge:
    """Pin cid into edge pinata remote cache

    Output:
        {
            "Status": "queued",
            "Cid": "QmZ4agkfrVHjLZUZ8EZnNqxeVfNW5YpxNaNYLy1fTjnYt1",
            "Name": ""
        }
        
    http://docs.ipfs.io/reference/cli/#ipfs-pin-remote-add
    :param cid: the cid to pin
    :param service: name of remote service
    :background: run pinning on background
    :return: ipfs output for remote pin
    :rtype: Edge
    """
    args = (
        cid,
        f"--service={service}",
        f"--background={background}",
    )

    # Exec command and get output
    exec = CLI("/pin/remote/add", args)
    output = exec().get("output")

    return Edge(
        status=output.get("Status"),  # status: queue using background
        cid=output.get("Cid"),  # resulting cid
        name=output.get("Name"),  # named pin
    )


def local(cid: CIDStr) -> Pin:
    """Pin cid into local node

    Output.
        {
            "Pins":["QmZ4agkfrVHjLZUZ8EZnNqxeVfNW5YpxNaNYLy1fTjnYt1"]
        }
        
    http://docs.ipfs.io/reference/cli/#ipfs-pin
    :param cid: the cid to pin
    :return: ipfs output for ipfs local pin
    :rtype: Pin
    """
    # Exec command and get output
    exec = CLI("/pin/add/", cid)
    output = exec().get("output")
    return Pin(pins=output.get("Pins"))
