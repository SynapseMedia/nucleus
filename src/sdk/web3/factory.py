from typing import Dict, Type, Any
from ...core.blockchain import ChainID, ContractID, NetworkID, Network, Chain, Contract
from ...core.blockchain.contracts import ERC1155
from ...core.blockchain.network import Ethereum
from ...core.blockchain.chains import Rinkeby, Goerli
from ...core.exceptions import (
    InvalidChain,
    InvalidNetwork,
    InvalidContract,
)


def chain(chain_id: ChainID) -> Chain:
    """Return chain by chain id. eg. Rinkeby, goerli, mainnet..

    :param chain_id: goerli- > 42,rinkeby -> 4...
    :return: Chain object based on chain id
    :rtype: Chain
    :raises InvalidChain
    """

    chains: Dict[ChainID, Type[Chain]] = {
        ChainID.Rinkeby: Rinkeby,
        ChainID.Goerli: Goerli,
    }

    if chain_id not in chains:
        raise InvalidChain("%s is not a valid network" % chain_id)

    chain_class = chains.get(chain_id, Rinkeby)
    return chain_class()


def network(net: NetworkID, **kwargs: Any) -> Network:
    """Return a network class based on chain

    :param net: Ethereum -> 0
    :return: Network object based on network id
    :rtype: Network
    :raises InvalidNetwork
    """
    networks: Dict[NetworkID, Type[Network]] = {NetworkID.Ethereum: Ethereum}

    if net not in networks:
        raise InvalidNetwork("%s is not a valid network" % net)

    network_class = networks.get(net, Ethereum)
    return network_class(**kwargs)


def contract(type: ContractID, **kwargs: Any) -> Contract:
    """Factory NFT contract based on provider settings

    :param type: The contract type eg. ERC1155 | ERC20 |
    :return: Contract object based on type
    :rtype: Contract
    :raises InvalidContract
    """
    contracts: Dict[ContractID, Type[Contract]] = {ContractID.ERC1155: ERC1155}

    if type not in contracts:
        raise InvalidContract("%s is not a valid contract standard" % type)

    contract_class = contracts.get(type, ERC1155)
    return contract_class(**kwargs)
