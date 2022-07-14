from web3.providers.rpc import HTTPProvider
from src.core.types import Endpoint
from src.core.constants import (
    WALLET_KEY,
    GOERLI_PROVIDER,
    GOERLI_ALCHEMY_API_KEY,
    RINKEBY_PROVIDER,
    RINKEBY_ALCHEMY_API_KEY,
    GOERLI_CONTRACT_NFT,
    RINKEBY_CONTRACT_NFT,
)

# package types
from .types import Chain, ChainID, Provider


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


class Goerli(Chain):
    """Goerli chain type"""

    def __str__(self):
        return "goerli"

    @property
    def id(self):
        return ChainID.Goerli

    @property
    def endpoint(self) -> Endpoint:
        return f"{GOERLI_PROVIDER}/{GOERLI_ALCHEMY_API_KEY}"

    @property
    def provider(self):
        """Return goerli pre-build Http Provider

        :return: goerli provider
        :rtype: Web3.HTTPProvider
        """

        return Web3HTTPProviderAdapter()

    @property
    def erc1155(self):
        return GOERLI_CONTRACT_NFT

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
