from src.sdk.constants import WALLET_KEY
from .factory import nft_contract
from web3 import Web3

import base58


def mint(to: str, cid: str, chain_name="kovan"):
    _w3, contract = nft_contract(chain_name)

    owner = _w3.eth.account.privateKeyToAccount(WALLET_KEY)
    nonce = _w3.eth.getTransactionCount(owner.address)
    cid = Web3.toHex(base58.b58decode(cid)[2:])
    to = Web3.toChecksumAddress(to)

    transaction = contract.functions.mint(to, cid).buildTransaction({"nonce": nonce})
    signed_txn = _w3.eth.account.sign_transaction(transaction, private_key=WALLET_KEY)
    return _w3.eth.send_raw_transaction(signed_txn.rawTransaction)


def mint_batch(to: str, cid_list: list, chain_name="kovan"):
    _w3, contract = nft_contract(chain_name)

    owner = _w3.eth.account.privateKeyToAccount(WALLET_KEY)
    nonce = _w3.eth.getTransactionCount(owner.address)
    cid_list_to_hex = [Web3.toHex(base58.b58decode(x)) for x in cid_list]

    transaction = contract.functions.mintBatch(to, cid_list_to_hex).buildTransaction(
        {"nonce": nonce}
    )
    signed_txn = _w3.eth.account.sign_transaction(transaction, private_key=WALLET_KEY)
    return _w3.eth.send_raw_transaction(signed_txn.rawTransaction)
