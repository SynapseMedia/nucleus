from src.sdk.constants import WALLET_KEY
from .factory import nft_contract
from .crypto import cid_to_uint256
from .. import logger


def mint(to: str, cid, chain_name="kovan"):
    """
    Mint token to address based on cid in defined chain
    :param to: receptor
    :param cid: IPFS cid
    :param chain_name: chain where mint the token
    :return: eth.Transaction
    """

    logger.log.info(f"Minting CID {cid} for {to} in {chain_name}")
    _w3, contract = nft_contract(chain_name)
    owner = _w3.eth.account.privateKeyToAccount(WALLET_KEY)
    nonce = _w3.eth.getTransactionCount(owner.address)

    cid = cid_to_uint256(cid)  # Format base16 => hex => int
    transaction = contract.functions.mint(to, cid).buildTransaction({"nonce": nonce})
    signed_txn = _w3.eth.account.sign_transaction(transaction, private_key=WALLET_KEY)
    tx = _w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    logger.log.info(f"Uint256 cid: {cid}")
    logger.log.info(f"NFT cid: {contract.functions.uri(cid).call()}")
    logger.log.info(f"TX: {tx.hex()}")

    return tx.hex()


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

    cid_list = [cid_to_uint256(x) for x in cid_list]  # Format base16 => hex => int
    transaction = contract.functions.mintBatch(to, cid_list).buildTransaction(
        {"nonce": nonce}
    )
    signed_txn = _w3.eth.account.sign_transaction(transaction, private_key=WALLET_KEY)
    tx = _w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    logger.log.info(f"TX: {tx.hex()}")
    return tx.hex()
