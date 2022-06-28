from ..types import CIDStr
from . import CLI, Edge, Pin, Service


def remote(cid: CIDStr, service: Service, background: bool) -> Edge:
    """Pin cid into edge pinata remote cache
    ref: http://docs.ipfs.io/reference/cli/#ipfs-pin-remote-add
    
    Output:
        {
            "Status": "queued",
            "Cid": "QmZ4agkfrVHjLZUZ8EZnNqxeVfNW5YpxNaNYLy1fTjnYt1",
            "Name": ""
        }
        

    :param cid: the cid to pin
    :param service: name of remote service
    :background: run pinning on background
    :return: ipfs output for remote pin
    :rtype: Edge
    :raises IPFSFailedExecution
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
    ref: http://docs.ipfs.io/reference/cli/#ipfs-pin

    Output:
        {
            "Pins":["QmZ4agkfrVHjLZUZ8EZnNqxeVfNW5YpxNaNYLy1fTjnYt1"]
        }
        
    :param cid: the cid to pin
    :return: ipfs output for ipfs local pin
    :rtype: Pin
    :raises IPFSFailedExecution
    """
    # Exec command and get output
    exec = CLI("/pin/add/", cid)
    output = exec().get("output")
    return Pin(pins=output.get("Pins"))
