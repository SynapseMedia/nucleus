from src.sdk.constants import WALLET_KEY, WALLET_PUBLIC_KEY
from .factory import nft_contract
from .crypto import cid_to_uint256
from .. import logger


def _show_stats(_w3, tx):
    """
    Show generic transaction stats
    :param _w3: Web3
    :param tx: Transaction hex to log
    """

    tx_details = _w3.eth.get_transaction(tx)
    logger.log.info(f"Owner: {WALLET_PUBLIC_KEY}")
    logger.log.info(f"Tx Gas #: {tx_details['gas']}")
    logger.log.info(f"Tx Gas Price #: {tx_details['gasPrice']}")
    logger.log.info(f"Tx Block Hash: {tx_details['blockHash']}")
    logger.log.info(f"Tx Block #: {tx_details['blockNumber']}")
    logger.log.info(f"Tx Nonce #: {tx_details['nonce']}")


def _send_tx(_w3, tx):
    """
    Commit transaction to blockchain
    :param _w3: Web3
    :param tx: Signed transaction
    """
    signed_txn = _w3.eth.account.sign_transaction(tx, private_key=WALLET_KEY)
    tx = _w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    logger.log.info(f"TX: {tx.hex()}")
    _show_stats(_w3, tx)  # Show additional generic stats
    return tx


def mint(to: str, cid, chain_name="kovan"):
    """
    Mint token to address based on cid in defined chain
    :param to: receptor
    :param cid: IPFS cid
    :param chain_name: chain where mint the token
    :return: eth.Transaction
    """

    logger.log.info(f"Minting CID {cid} in {chain_name}")
    _w3, contract = nft_contract(chain_name)
    owner = _w3.eth.account.privateKeyToAccount(WALLET_KEY)
    nonce = _w3.eth.getTransactionCount(owner.address)

    uint256_cid = cid_to_uint256(cid)  # Format base16 => hex => int
    transaction = contract.functions.mint(
        to, uint256_cid  # owner, cid uint256
    ).buildTransaction({"nonce": nonce})

    tx = _send_tx(_w3, transaction)
    return tx.hex(), to, cid


def mint_batch(to: str, cid_list: list, chain_name="kovan"):
    """
    Mint batch token to address based on cid list in defined chain
    :param to: receptor
    :param cid_list: IPFS cid
    :param chain_name: chain where mint the token
    :return: eth.Transaction
    """
    _w3, contract = nft_contract(chain_name)
    owner = _w3.eth.account.privateKeyToAccount(WALLET_KEY)
    nonce = _w3.eth.getTransactionCount(owner.address)

    uint256_cid_list = [
        cid_to_uint256(x) for x in cid_list
    ]  # Format base16 => hex => int
    transaction = contract.functions.mintBatch(
        to, uint256_cid_list  # owner, cid uint256
    ).buildTransaction({"nonce": nonce})

    tx = _send_tx(_w3, transaction)
    return tx.hex(), to, cid_list


def set_holder(to: str, cid: str, chain_name="kovan"):
    """
    Mint batch token to address based on cid list in defined chain
    :param to: receptor
    :param cid: IPFS cid
    :param chain_name: chain where mint the token
    :return: eth.Transaction
    """
    _w3, contract = nft_contract(chain_name)
    owner = _w3.eth.account.privateKeyToAccount(WALLET_KEY)
    nonce = _w3.eth.getTransactionCount(owner.address)

    uint256_cid = cid_to_uint256(cid)  # Format base16 => hex => int
    # Format base16 => hex => int
    transaction = contract.functions.setHolder(
        uint256_cid, to  # cid uint256, holder
    ).buildTransaction({"nonce": nonce})

    tx = _send_tx(_w3, transaction)
    return tx.hex(), to
