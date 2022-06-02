from . import chain
from .. import util
from ..constants import WALLET_KEY, PROJECT_ROOT
from ..exception import InvalidPrivateKey
from dataclasses import dataclass
from web3 import Web3
from eth_account import Account


@dataclass
class Web3Wrapper:
    """A data class to wrap web3 artifacts
    @param web3: The web3 instance
    @param chain: The current chain in use
    @param settings: The settings based on chain. eg. {"connector", "name", "private_key"}

    """

    web3: Web3
    chain: str
    settings: dict

    def __init__(self, w3: Web3, chain: str, settings: None):
        self.web3 = w3
        self.chain = chain
        self.settings = settings


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
    chain_settings = chain.get_network_settings_by_name(chain_name)
    # Connect to provider based on chain settings
    _w3 = Web3(chain_settings.get("connect")())
    # Set default account for current WALLET_KEY settings
    _w3.eth.default_account = account(chain_settings.get("private_key"))
    return Web3Wrapper(_w3, chain_name, chain_settings)


def nft_contract(chain_name: str, abi_path: str = PROJECT_ROOT):
    """Factory NFT contract based on provider settings

    :param chain_name: kovan, mainnet, rinkeby...
    :return: w3 interface, nft contract
    :rtype: Union[Web3, web3.eth.Contract]
    """

    w3_wrapper = w3(chain_name)
    # Get contract address based on chain settings
    chain_contract_nft = w3_wrapper.settings.get("nft")
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
