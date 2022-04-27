from cid import make_cid
from web3 import Web3


def to_hex(_input: str):
    """Convert input to hex representation

    :param _input:
    :return: Hexadecimal string
    :rtype: str
    """
    return Web3.toHex(_input)


def cid_to_uint256(cid: str):
    """Encode cid to uint256

    :param cid: IPFS cid
    :return: uint256 cid representation
    :rtype: int
    """
    cid_base16 = make_cid(cid).encode("base16")
    return int("0x" + cid_base16[1:].decode("utf-8"), 0)
