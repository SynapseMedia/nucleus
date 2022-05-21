from eth_account import Account
from ..exception import InvalidPrivateKey, InvalidProvider
from ..constants import WALLET_KEY, KOVAN, RINKEBY, ERC_1155

from .contracts import NFT
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
    :return: blockchain based on chain id
    :rtype: Blockchain
    """

    # Get chain settings from chain name
    chain_object = chain(chain_id)
    # Blockchain factory
    blockchain_class = blockchain(chain_id)
    # Connect to provider based on chain settings
    _blockchain = blockchain_class(chain_object)
    _blockchain.set_default_account(chain_object.private_key)
    return _blockchain


def contract(chain_id: int, type: str = ERC_1155):
    """Factory NFT contract based on provider settings

    :param chain_id: kovan=42, rinkeby=4...
    :param type: The contract type eg. ERC1155 | ERC20 |
    :return: w3 interface, nft contract
    :rtype: web3.eth.Contract
    """

    _blockchain = blockchain(chain_id)
    return {ERC_1155: NFT(_blockchain)}.get(type)
