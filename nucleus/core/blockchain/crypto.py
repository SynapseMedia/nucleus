# Convention for importing types
from web3 import Web3

from nucleus.core.types import CID, HexStr, Primitives


def to_hex(input_: Primitives) -> HexStr:
    """Convert input to hex representation

    :param input:
    :return: hexadecimal string
    :rtype: str
    """
    return HexStr(Web3.to_hex(input_))


def cid_to_uint256(cid_: CID) -> int:
    """Encode cid to uint256

    :param cid: IPFS cid
    :return: uint256 cid representation
    :rtype: int
    """
    cid_base16 = cid_.format().encode('base16')
    return int('0x' + cid_base16[1:], 0)
