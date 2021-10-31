from src.sdk.constants import WALLET_KEY
from .factory import nft_contract
from .crypto import base58_to_hex
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
    cid = base58_to_hex(cid)

    logger.log.info(f"Hex: {cid}")
    logger.log.info(f"uint256: {int(cid, 0)}")

    transaction = contract.functions.mint(to, int(cid, 0)).buildTransaction(
        {"nonce": nonce}
    )

    signed_txn = _w3.eth.account.sign_transaction(transaction, private_key=WALLET_KEY)
    return _w3.eth.send_raw_transaction(signed_txn.rawTransaction)


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
    cid_list_to_hex = [int(base58_to_hex(x), 0) for x in cid_list]

    transaction = contract.functions.mintBatch(to, cid_list_to_hex).buildTransaction(
        {"nonce": nonce}
    )

    signed_txn = _w3.eth.account.sign_transaction(transaction, private_key=WALLET_KEY)
    return _w3.eth.send_raw_transaction(signed_txn.rawTransaction)
