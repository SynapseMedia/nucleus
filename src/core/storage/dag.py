from ..types import CIDStr
from . import CLI, Dag, DagLink


def get(cid: CIDStr) -> Dag:
    """Retrieve dag information from cid

    Output:
        {
            "Data": {"/": {"bytes": "CAIY1qEQIICAECDWIQ"}},
            "Links": [
                {
                    "Hash": {"/": "QmRoo28ogKQ6ds3jk9x7X7x3sjTs2yTMu5vHUPxLN8vinU"},
                    "Name": "",
                    "Tsize": 262158,
                },
            ],
        }
        
    https://docs.ipfs.io/reference/cli/#ipfs-dag-get
    :param cid: cid to retrieve from dag
    :return: Dag representation objects
    :rtype: Dag
    """

    # Exec command and get output
    exec = CLI("/dag/get", cid)
    output = exec().get("output")
    links = map(lambda l: DagLink(**l), output.get("Links"))

    return Dag(data=output.get("Data"), links=links)
