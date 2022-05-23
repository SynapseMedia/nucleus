from eth_account import Account
from ..exception import InvalidPrivateKey, InvalidChain, InvalidBlockChain
from ..constants import WALLET_KEY

from . import ChainID, Chain, ContractStandards, Network
from .contracts import NFT
from .network import Ethereum
from .chains import Rinkeby, Kovan


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


def chain(network: ChainID):
    """Return chain by chain id. eg. Rinkeby, kovan, mainnet..

    :param network: kovan- > 42,rinkeby -> 4...
    :return: network settings based on provider name
    :rtype: Chain
    """

    networks = {
        ChainID.RINKEBY: Rinkeby(),
        ChainID.KOVAN: Kovan(),
    }

    if network not in networks:
        raise InvalidChain("%s is not a valid network" % network)
    return networks[network]


def network(chain: Chain):
    """Return a network class based on chain

    :param chain: kovan- > 42,rinkeby -> 4
    :return: Network object
    :rtype: Network
    """
    allowed_networks = {
        ChainID.KOVAN: Ethereum,
        ChainID.RINKEBY: Ethereum,
    }

    if chain.id not in allowed_networks:
        raise InvalidBlockChain("%s is not a valid network" % chain)

    network_class = allowed_networks[chain.id]
    return network_class(chain)


def w3(chain_id: ChainID):
    """Build a Web3 network interface based on chain id

    :param _chain_id: eg.kovan, mainnet, rinkeby...
    :return: network based on chain id
    :rtype: Network
    """

    # Blockchain builder
    # Get chain settings from chain name
    _chain = chain(chain_id)
    _network = network(_chain)
    # Connect to provider based on chain settings
    _account = account(_network.chain.private_key)
    _network.set_default_account(_account)
    # ...any method needed to config blockchain could be here...
    return _network


def contract(network: Network, type: ContractStandards):
    """Factory NFT contract based on provider settings

    :param network: Ethereum, Algorand, etc..
    :param type: The contract type eg. ERC1155 | ERC20 |
    :return: nft contract
    :rtype: web3.eth.Contract
    """

    # TODO add exception when doesnt exist contract
    return {ContractStandards.ERC1155: NFT(network)}.get(type)
