from web3 import Web3, types
from .factory import nft_contract
from .crypto import cid_to_uint256
from ..constants import WALLET_KEY
from .. import logger


def _send_tx(w3: Web3, tx: types.TxData):
    """Commit transaction to blockchain

    :param w3: web3 interface
    :param tx: transaction summary
    :return: transaction hex string
    :rtype: str
    """
    signed_txn = w3.eth.account.sign_transaction(tx, private_key=WALLET_KEY)
    tx = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    logger.log.info(f"TX: {tx.hex()}")
    return tx


def mint(to: str, cid: str, chain_name: str = "kovan"):
    """Mint token to address based on cid in defined chain

    :param to: receptor
    :param cid: IPFS cid
    :param chain_name: chain where mint the token
    :return: tuple with (transaction address, receptor address, cid)
    :rtype: Union[str, str, str]
    """

    logger.log.info(f"Minting CID {cid} in {chain_name}")
    web3, contract = nft_contract(chain_name)

    # Format base16 => hex => int
    uint256_cid = cid_to_uint256(cid)
    transaction = contract.functions.mint(
        to, uint256_cid  # owner, cid uint256
    ).buildTransaction()

    tx = _send_tx(web3, transaction)
    return tx.hex(), to, cid


def mint_batch(to: str, cid_list: list, chain_name: str = "kovan"):
    """Mint batch token to address based on cid list in defined chain

    :param to: Receptor address
    :param cid_list: IPFS cid list
    :param chain_name: Chain name eg. Rinkeby
    :return: tuple with (transaction address, receptor address, cid list)
    :rtype: Union[str, str, list]
    """

    web3, contract = nft_contract(chain_name)
    # Format base16 => hex => int
    uint256_cid_list = [cid_to_uint256(x) for x in cid_list]

    transaction = contract.functions.mintBatch(
        to, uint256_cid_list  # owner, cid uint256
    ).buildTransaction()

    tx = _send_tx(web3, transaction)
    return tx.hex(), to, cid_list


def set_holder(to: str, cid: str, chain_name: str = "kovan"):
    """Mint batch token to address based on cid list in defined chain

    :param to: Receptor address
    :param cid: IPFS cid
    :param chain_name: Chain name eg. Rinkeby
    :return: tuple with (transaction address, receptor address)
    :rtype: Union[str, str]
    """
    
    web3, contract = nft_contract(chain_name)
    # Format base16 => hex => int
    uint256_cid = cid_to_uint256(cid)
    # Format base16 => hex => int
    transaction = contract.functions.setHolder(
        uint256_cid, to  # cid uint256, holder
    ).buildTransaction()

    tx = _send_tx(web3, transaction)
    return tx.hex(), to
