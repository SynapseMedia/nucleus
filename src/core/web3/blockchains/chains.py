from web3 import Web3

from . import Chain
from ...constants import (
    WALLET_KEY,
    KOVAN_PROVIDER,
    KOVAN_ALCHEMY_API_KEY,
    RINKEBY_PROVIDER,
    RINKEBY_ALCHEMY_API_KEY,
    WALLET_KEY,
    KOVAN_CONTRACT_NFT,
    RINKEBY_CONTRACT_NFT,
)


class EVM(Chain):
    pass


class Kovan(EVM):
    """Kovan chain type"""
    
    def connector(self):
        """Return kovan pre-build Http Provider

        :return: kovan provider
        :rtype: Web3.HTTPProvider
        """
        return Web3.HTTPProvider(
            # Kovan alchemy endpoint
            f"{KOVAN_PROVIDER}/{KOVAN_ALCHEMY_API_KEY}"
        )

    @property
    def erc1155(self):
        return KOVAN_CONTRACT_NFT

    @property
    def private_key(self):
        return WALLET_KEY


class Rinkeby(EVM):
    """Rinkeby chain type"""
    
    def connector(self):
        """Return rinkeby pre-build Http Provider

        :return: rinkeby provider
        :rtype: Web3.HTTPProvider
        """
        return Web3.HTTPProvider(
            # Rinkeby alchemy endpoint
            f"{RINKEBY_PROVIDER}/{RINKEBY_ALCHEMY_API_KEY}"
        )

    @property
    def erc1155(self):
        return RINKEBY_CONTRACT_NFT

    @property
    def private_key(self):
        return WALLET_KEY
