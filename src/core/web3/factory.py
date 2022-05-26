from eth_account import Account
from ..exceptions import (
    InvalidPrivateKey,
    InvalidChain,
    InvalidNetwork,
    InvalidContract,
)
from ..constants import WALLET_KEY

from . import ChainID, ContractID, Network, NetworkID, Chain
from .contracts import NFT
from .network import Ethereum
from .chains import Rinkeby, Kovan


def account(private_key: str = WALLET_KEY):
    """Returns wrapped account from private key

    :param web: Web3 instance
    :param private_key: wallet key address
    :return: account object
    :rtype: Account
    :raises InvalidPrivateKey
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


def chain(chain_id: ChainID):
    """Return chain by chain id. eg. Rinkeby, kovan, mainnet..

    :param chain_id: kovan- > 42,rinkeby -> 4...
    :return: network settings based on provider name
    :raises InvalidChain
    :rtype: Chain
    """

    chains = {
        ChainID.Rinkeby: Rinkeby,
        ChainID.Kovan: Kovan,
    }

    if chain_id not in chains:
        raise InvalidChain("%s is not a valid network" % chain_id)

    chain_class = chains.get(chain_id)
    return chain_class()


def network(net: NetworkID, chain: Chain):
    """Return a network class based on chain

    :param net: Ethereum -> 0
    :param chain: chain to bind network eg. Rinkeby
    :return: Network object
    :raises InvalidNetwork
    :rtype: Network
    """
    networks = {NetworkID.Ethereum: Ethereum}

    if net not in networks:
        raise InvalidNetwork("%s is not a valid network" % net)

    network_class = networks.get(net)
    return network_class(chain)


def contract(type: ContractID, network: Network):
    """Factory NFT contract based on provider settings

    :param type: The contract type eg. ERC1155 | ERC20 |
    :param network: Ethereum, Algorand, etc..
    :return: nft contract
    :raises InvalidContract
    :rtype: Contract
    """
    contracts = {ContractID.ERC1155: NFT}

    if type not in contracts:
        raise InvalidContract("%s is not a valid contract standard" % type)

    contract_class = contracts.get(type)
    return contract_class(network)
