from web3 import Web3
from .chains import EVM
from . import Network
from ..types import Address, Request, Hash, Abi


class Ethereum(Network):
    """Ethereum network type"""

    web3: Web3

    def __init__(self, chain: EVM):
        # Connect network to chain provider
        if not isinstance(chain, EVM):
            raise TypeError("provided `chain` for ethereum network not supported")

        super().__init__(chain)
        self.web3 = Web3(chain.connector())

    def set_default_account(self, account: Address):
        self.web3.eth.default_account = account
        return account

    def sign_transaction(self, tx: Request):
        return self.web3.eth.account.sign_transaction(
            tx, private_key=self.chain.private_key
        )

    def get_transaction(self, hash: Hash):
        return self.web3.eth.get_transaction(hash)

    def send_transaction(self, tx: Request):
        # Return result from commit signed transaction
        signed_tx = self.sign_transaction(tx)
        transaction = signed_tx.rawTransaction
        return self.web3.eth.send_raw_transaction(transaction)

    def contract(self, address: Address, abi: Abi):
        return self.web3.eth.contract(
            # Contract address
            address=Web3.toChecksumAddress(address),
            # Abi from contract deployed
            abi=abi,
        )
