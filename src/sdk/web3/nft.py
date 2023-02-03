from src.core.blockchain import ContractID, ChainID
from src.core.blockchain.factory import contract, w3
from src.core.blockchain.crypto import cid_to_uint256
from src.sdk import logger

# TODO add NFT type that define methods


def mint(to: str, cid: str, chain_id: ChainID):
    """Mint token to address based on cid in defined chain

    :param to: receptor
    :param cid: IPFS cid
    :param chain_id: Chain id eg. 4 -> Rinkeby
    :return: Transaction summary
    :rtype: TxData
    """

    logger.log.info(f"Minting CID {cid} in {chain_id}")

    network = w3(chain_id)  # Network from chain id
    _contract = contract(network, ContractID.ERC1155)

    # Format base16 => hex => int
    uint256_cid = cid_to_uint256(cid)

    # Build contract transaction call
    # owner, cid uint256
    tx = _contract.mint(to, uint256_cid).buildTransaction()

    tx = network.send_transaction(tx)
    return network.get_transaction(tx.hex())


def mint_batch(to: str, cid_list: list, chain_id: int = 4):
    """Mint batch token to address based on cid list in defined chain

    :param to: Receptor address
    :param cid_list: IPFS cid list
    :param chain_id: Chain id eg. 4 -> Rinkeby
    :return: tuple with (transaction address, receptor address, cid list)
    :rtype: Union[str, str, list]
    """

    contract = nft_contract(chain_id)
    # Format base16 => hex => int
    uint256_cid_list = map(cid_to_uint256, cid_list)

    tx = contract.functions.mintBatch(
        to, uint256_cid_list  # owner, cid uint256
    ).buildTransaction()

    tx = transaction(chain_id, tx)
    return tx.hex(), to, cid_list


def set_holder(to: str, cid: str, chain_id: id = 4):
    """Mint batch token to address based on cid list in defined chain

    :param to: Receptor address
    :param cid: IPFS cid
    :param chain_id: Chain id eg. 4 -> Rinkeby
    :return: tuple with (transaction address, receptor address)
    :rtype: Union[str, str]
    """

    contract = nft_contract(chain_id)
    # Format base16 => hex => int
    uint256_cid = cid_to_uint256(cid)
    # Format base16 => hex => int
    tx = contract.functions.setHolder(
        uint256_cid, to  # cid uint256, holder
    ).buildTransaction()

    tx = transaction(chain_id, tx)
    return tx.hex(), to
