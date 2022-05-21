from re import L
from web3 import Web3
from eth_account import Account

from .. import util
from ..exception import InvalidPrivateKey, InvalidProvider
from ..constants import WALLET_KEY, KOVAN, RINKEBY

from .blockchains.blockchain import Ethereum
from .blockchains.chains import Rinkeby, Kovan


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


def chain(chain_id: int):
    """Return network settings by provider name. eg. Rinkeby, kovan, mainnet..

    :param chain_id: kovan- > 42,rinkeby -> 4...
    :return: network settings based on provider name
    :rtype: Chain
    """

    providers = {
        KOVAN: Rinkeby(),
        RINKEBY: Kovan(),
    }

    # Provider not found from web3 import Web3, types
    if chain_id not in providers:
        raise InvalidProvider("%s is not a valid provider name" % chain_id)
    return providers[chain_id]


def blockchain(chain_id: int):
    """Return a blockchain class from chain id

    :param chain_id: kovan- > 42,rinkeby -> 4
    :return: Blockchain class
    :rtype: Blockchain
    """
    return {KOVAN: Ethereum, RINKEBY: Ethereum}.get(chain_id, Ethereum)


def w3(chain_id: int):
    """Build Web3 interface with provider settings

    :param chain_id: kovan, mainnet, rinkeby...
    :return: web3 interface with provider settings
    :rtype: Web3Wrapper
    """

    # Get chain settings from chain name
    chain_object = chain(chain_id)
    # Blockchain factory
    blockchain_class = blockchain(chain_id)
    # Connect to provider based on chain settings
    blockchain = blockchain_class(chain_object)
    blockchain.set_default_account(chain_object.private_key)
    return blockchain


# TODO refactor to Contract abstract factory eg. NFT | ERC20
def contract(chain_id: int, abi_path: str = PROJECT_ROOT):
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
