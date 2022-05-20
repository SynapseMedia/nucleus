from web3 import Web3, types
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
        self.nft = nft
        self.connector = connector
        self.private_key = private_key


class Web3Wrapper:
    """A class wrapper for web3 artifacts
    @param web3: The web3 instance
    @param chain_id: The current chain id in use eg. 4 -> rinkeby
    @param chain: The settings based on chain. eg. {"connector", "name", "private_key"}
    
    In the future this class can hold a creational pattern for diff chains
    """

    web3: Web3
    chain_id: int
    chain: ChainWrapper

    def __init__(self, w3: Web3, chain_id: int, settings: None):
        self.web3 = w3
        self.chain_id = chain_id
        self.chain = settings


# TODO write tests.. not a factory move out
def transaction(chain_id: int, tx: types.TxData):
    """Commit transaction to blockchain

    :param chain_id: chain where the transaction will be sent
    :param tx: transaction summary
    :return: transaction hex string
    :rtype: HexBytes
    """
    _web3 =  w3(chain_id).web3
    # Sign transaction with private key
    signed_txn = _web3.eth.account.sign_transaction(tx, private_key=WALLET_KEY)
    # Return result from commit signed transaction
    return _web3.eth.send_raw_transaction(signed_txn.rawTransaction)


def chain(chain_id: int):
    """Return network settings by provider name. eg. Rinkeby, kovan, mainnet..

    :param chain_id: kovan- > 42,rinkeby -> 4...
    :return: network settings based on provider name
    :rtype: Chain
    """

    providers = {
        KOVAN: ChainWrapper(_kovan, KOVAN_CONTRACT_NFT, WALLET_KEY),
        RINKEBY: ChainWrapper(_rinkeby, RINKEBY_CONTRACT_NFT, WALLET_KEY),
    }

    # Provider not found from web3 import Web3, types
    if chain_id not in providers:
        raise InvalidProvider("%s is not a valid provider name" % chain_id)
    return providers[chain_id]


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


def w3(chain_id: int):
    """Build Web3 interface with provider settings

    :param chain_id: kovan, mainnet, rinkeby...
    :return: web3 interface with provider settings
    :rtype: Web3Wrapper
    """

    # Get chain settings from chain name
    chain_settings = chain(chain_id)
    # Connect to provider based on chain settings
    _w3 = Web3(chain_settings.connector())
    # Set default account for current WALLET_KEY settings
    _w3.eth.default_account = account(chain_settings.private_key)
    return Web3Wrapper(_w3, chain_id, chain_settings)


# TODO refactor to Contract Builder eg. NFT | ERC20
def nft_contract(chain_id: int, abi_path: str = PROJECT_ROOT):
    """Factory NFT contract based on provider settings

    :param chain_id: kovan=42, rinkeby=4...
    :param abi_path: The json abi path to use for contract
    :return: w3 interface, nft contract
    :rtype: web3.eth.Contract
    """

    w3_wrapper = w3(chain_id)
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

    return contract
