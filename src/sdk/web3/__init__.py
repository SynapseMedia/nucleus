import os
from web3 import Web3

KOVAN_TESTNET = os.getenv("KOVAN_PROVIDER", "")


def kovan_provider():
    return Web3.HTTPProvider(f"{KOVAN_TESTNET}")


def web3_factory(provider):
    w3 = Web3(provider)
    return w3
