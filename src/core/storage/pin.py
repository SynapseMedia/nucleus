from ..types import RemotePin, Pin
from . import CLI


def remote(cid: str, service: str, background: bool) -> RemotePin:
    """Pin cid into edge pinata remote cache

    http://docs.ipfs.io/reference/cli/#ipfs-pin-remote-add
    :param cid: the cid to pin
    :param service: name of remote service
    :background: run pinning on background
    :return: ipfs output for remote pin
    :rtype: PinRemote
    """
    args = (
        cid,
        f"--service={service}",
        f"--background={background}",
    )

    # Exec command and get output
    exec = CLI("/pin/remote/add", args)
    output = exec().get("result")

    return RemotePin(
        status=output.get("Status"),  # status: queue using background
        cid=output.get("Cid"),  # resulting cid
        name=output.get("Name"),  # named pin
    )


def local(cid: str) -> Pin:
    """Pin cid into local node

    http://docs.ipfs.io/reference/cli/#ipfs-pin
    :param cid: the cid to pin
    :return: ipfs output for ipfs local pin
    """
    # Exec command and get output
    exec = CLI("/pin/add/", cid)
    output = exec().get("result")

    return Pin(pins=output.get("Pins"))
