from web3 import Web3
from typing import Callable
from eth_account import Account

from .. import util
from ..exception import InvalidPrivateKey, InvalidProvider
from ..constants import (
    WALLET_KEY,
    PROJECT_ROOT,
    KOVAN_PROVIDER,
    KOVAN_CONTRACT_NFT,
    KOVAN_ALCHEMY_API_KEY,
    RINKEBY_PROVIDER,
    RINKEBY_ALCHEMY_API_KEY,
    RINKEBY_CONTRACT_NFT,
    WALLET_KEY,
    KOVAN,
    RINKEBY,
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


class ChainWrapper:
    """A class wrapper for Chain settings
    @param connector: The web3 provider
    @param private_key: The private key for network
    @param nft: Nft contract address for chain

    """
    connector: Callable
    private_key: str
    nft: str

    def __init__(self, connector, nft, private_key):
        self.connector = connector
        self.nft = nft
        self.private_key = private_key


class Web3Wrapper:
    """A class wrapper for web3 artifacts
    @param web3: The web3 instance
    @param name: The current chain in use
    @param chain: The settings based on chain. eg. {"connector", "name", "private_key"}

    """

    web3: Web3
    name: str
    chain: ChainWrapper

    def __init__(self, w3: Web3, chain: str, settings: None):
        self.web3 = w3
        self.name = chain
        self.chain = settings


def chain(provider_name: str):
    """Return network settings by provider name. eg. Rinkeby, kovan, mainnet..

    :param: provider_name: Name of the provider to retrieve settings.
    :return: network settings based on provider name
    :rtype: Chain
    """

    providers = {
        KOVAN: ChainWrapper(**{
            "connector": _kovan,
            "nft": KOVAN_CONTRACT_NFT,
            "private_key": WALLET_KEY,
        }),
        RINKEBY: ChainWrapper(**{
            "connector": _rinkeby,
            "nft": RINKEBY_CONTRACT_NFT,
            "private_key": WALLET_KEY,
        }),
    }

    # Provider not found
    if provider_name not in providers:
        raise InvalidProvider("%s is not a valid provider name" % provider_name)
    return providers[provider_name]



def account(private_key: str = WALLET_KEY):
    """Returns wrapped account from private key

    :param web: Web3 instance
    :param private_key: wallet key address
    :return: account object
    :rtype: web3.Account
    """
    if not private_key:
        raise InvalidPrivateKey()

    # Append hex prefix to key if not found
    if private_key[:2] != "0x":
        private_key = "0x%s" % private_key

    try:
        return Account.from_key(private_key)
    except ValueError as e:
        raise InvalidPrivateKey(e)


def w3(chain_name: str):
    """Build Web3 interface with provider settings

    :param chain_name: kovan, mainnet, rinkeby...
    :return: web3 interface with provider settings
    :rtype: Web3Wrapper
    """

    # Get chain settings from chain name
    chain_settings = chain(chain_name)
    # Connect to provider based on chain settings
    _w3 = Web3(chain_settings.connector())
    # Set default account for current WALLET_KEY settings
    _w3.eth.default_account = account(chain_settings.private_key)
    return Web3Wrapper(_w3, chain_name, chain_settings)


def nft_contract(chain_name: str, abi_path: str = PROJECT_ROOT):
    """Factory NFT contract based on provider settings

    :param chain_name: kovan, mainnet, rinkeby...
    :return: w3 interface, nft contract
    :rtype: Union[Web3, web3.eth.Contract]
    """

    w3_wrapper = w3(chain_name)
    # Get contract address based on chain settings
    chain_contract_nft = w3_wrapper.chain.nft
    abi = util.read_json("%s/abi/WNFT.json" % abi_path)

    # Web3 instance
    web3_object = w3_wrapper.web3
    # web3 contract factory
    contract = web3_object.eth.contract(
        # Contract address
        address=Web3.toChecksumAddress(chain_contract_nft),
        # Abi from contract deployed
        abi=abi.get("abi"),
    )

    return web3_object, contract

