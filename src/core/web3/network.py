from web3 import Web3
from eth_typing.evm import ChecksumAddress


from .chains import EVM
from . import Network, ProxyContract
from ..types import Address, TxCall, Hash, Abi, TxAnswer


class Ethereum(Network):
    """Ethereum network type"""

    web3: Web3

    def __init__(self, chain: EVM):
        super().__init__(chain)
        self.web3 = Web3(chain.connector())

    def set_default_account(self, account: Address):
        self.web3.eth.default_account = ChecksumAddress(account)

    def sign_transaction(self, tx: TxCall):
        return self.web3.eth.account.sign_transaction(
            tx, private_key=self.chain.private_key
        )

    def get_transaction(self, hash: Hash):
        return TxAnswer(self.web3.eth.get_transaction(hash))

    def send_transaction(self, tx: TxCall):
        # Return result from commit signed transaction
        signed_tx = self.sign_transaction(tx)
        transaction = signed_tx.rawTransaction
        return self.web3.eth.send_raw_transaction(transaction)

    def build_contract(self, address: Address, abi: Abi):
        return ProxyContract(
            self.web3.eth.contract(
                # Contract address
                address=Web3.toChecksumAddress(address),
                # Abi from contract deployed
                abi=abi,
            )
        )
