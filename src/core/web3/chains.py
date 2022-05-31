from web3.providers.rpc import HTTPProvider

from . import Chain, ChainID, Provider
from ..types import Endpoint
from ..constants import (
    WALLET_KEY,
    KOVAN_PROVIDER,
    KOVAN_ALCHEMY_API_KEY,
    RINKEBY_PROVIDER,
    RINKEBY_ALCHEMY_API_KEY,
    KOVAN_CONTRACT_NFT,
    RINKEBY_CONTRACT_NFT,
)


class Web3HTTPProviderAdapter(Provider):
    """Explicitly http provider implementation

    refs:
        - https://peps.python.org/pep-0544/#defining-a-protocol
        - https://www.geeksforgeeks.org/adapter-method-python-design-patterns/
    """

    def __call__(self):
        def __connect(endpoint: Endpoint) -> HTTPProvider:
            return HTTPProvider(endpoint)
        return __connect


class Kovan(Chain):
    """Kovan chain type"""

    def __str__(self):
        return "kovan"

    @property
    def id(self):
        return ChainID.Kovan

    @property
    def endpoint(self) -> Endpoint:
        return f"{KOVAN_PROVIDER}/{KOVAN_ALCHEMY_API_KEY}"

    @property
    def provider(self):
        """Return kovan pre-build Http Provider

        :return: kovan provider
        :rtype: Web3.HTTPProvider
        """

        return Web3HTTPProviderAdapter()

    @property
    def erc1155(self):
        return KOVAN_CONTRACT_NFT

    @property
    def private_key(self):
        return WALLET_KEY


class Rinkeby(Chain):
    """Rinkeby chain type"""

    def __str__(self):
        return "rinkeby"

    @property
    def id(self):
        return ChainID.Rinkeby

    @property
    def endpoint(self) -> Endpoint:
        return f"{RINKEBY_PROVIDER}/{RINKEBY_ALCHEMY_API_KEY}"

    @property
    def provider(self):
        """Return rinkeby pre-build Http Provider

        :return: rinkeby provider
        :rtype: Web3.HTTPProvider
        """
        return Web3HTTPProviderAdapter()

    @property
    def erc1155(self):
        return RINKEBY_CONTRACT_NFT

    @property
    def private_key(self):
        return WALLET_KEY
