import base58
from web3 import Web3


def base58_to_hex(b58):
    """
    Encode base58 to hex => uint256
    :param b58: string to encode
    :return: Hex string
    """
    return Web3.toHex(base58.b58decode(b58)[2:])
