from ..types import Edge, Pin
from . import CLI

def dag_get(cid: str):
    """Retrieve dag information from cid

    Proxy dag get command to node
    http://docs.ipfs.io.ipns.localhost:8080/reference/cli/#ipfs-dag-get
    :param cid:
    """
    return exec_command("/dag/get", cid)
