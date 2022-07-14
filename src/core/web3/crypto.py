import cid  # type: ignore
from web3 import Web3
from src.core.types import Primitives, HexStr, CIDStr


def to_hex(_input: Primitives) -> HexStr:
    """Convert input to hex representation

    :param _input:
    :return: Hexadecimal string
    :rtype: str
    """
    return HexStr(Web3.toHex(_input))


def cid_to_uint256(_cid: CIDStr) -> int:
    """Encode cid to uint256

    :param cid: IPFS cid
    :return: uint256 cid representation
    :rtype: int
    """
    _cid = cid.make_cid(_cid)  # type: ignore
    cid_base16 = _cid.encode("base16")  # type: ignore
    return int("0x" + cid_base16[1:].decode("utf-8"), 0)  # type: ignore
