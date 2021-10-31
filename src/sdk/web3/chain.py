from web3 import Web3
from src.sdk.constants import (
    KOVAN_PROVIDER,
    KOVAN_CONTRACT_NFT,
    KOVAN_ALCHEMY_API_KEY,
    RINKEBY_PROVIDER,
    RINKEBY_ALCHEMY_API_KEY,
    RINKEBY_CONTRACT_NFT,
)


def _kovan() -> Web3.HTTPProvider:
    """
    Return kovan pre-build Http Provider
    :return: Web2.HTTPProvider
    """
    return Web3.HTTPProvider(
        # Kovan alchemy endpoiny
        f"{KOVAN_PROVIDER}/{KOVAN_ALCHEMY_API_KEY}"
    )


def _rinkeby() -> Web3.HTTPProvider:
    """
    Return kovan pre-build Http Provider
    :return: Web2.HTTPProvider
    """
    return Web3.HTTPProvider(
        # Kovan alchemy endpoiny
        f"{RINKEBY_PROVIDER}/{RINKEBY_ALCHEMY_API_KEY}"
    )


def get_network_settings_by_name(provider_name: str) -> Web3.HTTPProvider:
    """
    Return network settings by provider name
    """
    providers = {
        "kovan": {"connect": _kovan, "nft": KOVAN_CONTRACT_NFT},
        "rinkeby": {"connect": _rinkeby, "nft": RINKEBY_CONTRACT_NFT},
        "mainnet": None,
    }

    if provider_name in providers:
        return providers[provider_name]
