from web3 import Web3
from ..exception import InvalidProvider
from ..constants import (
    KOVAN_PROVIDER,
    KOVAN_CONTRACT_NFT,
    KOVAN_ALCHEMY_API_KEY,
    RINKEBY_PROVIDER,
    RINKEBY_ALCHEMY_API_KEY,
    RINKEBY_CONTRACT_NFT,
)


def _kovan():
    """Return kovan pre-build Http Provider

    :return: kovan provider
    :rtype: Web3.HTTPProvider
    """
    return Web3.HTTPProvider(
        # Kovan alchemy endpoint
        f"{KOVAN_PROVIDER}/{KOVAN_ALCHEMY_API_KEY}"
    )


def _rinkeby():
    """Return kovan pre-build Http Provider

    :return: rinkeby provider
    :rtype: Web3.HTTPProvider
    """
    return Web3.HTTPProvider(
        # Rinkeby alchemy endpoint
        f"{RINKEBY_PROVIDER}/{RINKEBY_ALCHEMY_API_KEY}"
    )


def get_network_settings_by_name(provider_name: str):
    """Return network settings by provider name. eg. Rinkeby, kovan, mainnet..

    :param: provider_name: Name of the provider to retrieve settings.
    :return: network settings based on provider name
    :rtype: dict
    """

    providers = {
        "kovan": {"connect": _kovan, "nft": KOVAN_CONTRACT_NFT},
        "rinkeby": {"connect": _rinkeby, "nft": RINKEBY_CONTRACT_NFT},
        "mainnet": None,
    }

    if provider_name not in providers:
        raise InvalidProvider("%s is not a valid provider name" % provider_name)
    return providers[provider_name]
