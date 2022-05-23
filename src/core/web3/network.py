from web3 import Web3, types
from eth_account import Account
from .chains import EVM
from . import Network


class Ethereum(Network):
    """Ethereum network type"""

    def __init__(self, chain: EVM):
        super().__init__(chain)
        self.connect(chain)

    def connect(self, chain: EVM):
        self.web3 = Web3(chain.connector())

    def set_default_account(self, account: Account):
        self.web3.eth.default_account = account
        return account

    def sign_transaction(self, tx: types.TxParams):
        return self.web3.eth.account.sign_transaction(
            tx, private_key=self.chain.private_key
        )

    def send_transaction(self, tx: types.TxParams):
        # Return result from commit signed transaction
        signed_tx = self.sign_transaction(tx)
        return self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    def contract(self, address: str, abi: str):
        return self.web3.eth.contract(
            # Contract address
            address=Web3.toChecksumAddress(address),
            # Abi from contract deployed
            abi=abi,
        )
