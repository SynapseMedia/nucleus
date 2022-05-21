from abc import ABC, abstractmethod
from eth_account import Account


class Chain(ABC):
    """Chain abstract class

    Hold/specify the artifacts/methods needed to interact with chain.
    Use this class to create chain subtypes.

    Usage:
        class Kovan(Chain):
            ....

    """

    @abstractmethod
    def connector(self):
        """Return the connector interface
        
        Provide a connector to interact with chain.
        eg. Http | Websocket
        """
        pass

    @property
    @abstractmethod
    def private_key(self):
        """Return specific private key for chain
        
        :return: private key
        :rtype: str
        """
        pass

    @property
    @abstractmethod
    def erc1155(self):
        """Return address for deployed contract standard ERC1155 
        
        :return: nft contract address
        :rtype: str
        """
        pass


class Blockchain(ABC):
    """Blockchain abstract class

    Specify all methods needed to interact with the blockchain.
    Use this class to create blockchain subtypes.

    Usage:
        class Algorand(Blockchain):
            ....

    """

    def __init__(self, chain: Chain):
        self.chain = chain
        super().__init__()

    @abstractmethod
    def set_default_account(self, account: Account):
        """Set default account for blockchain operations
        
        :param account: The account to subscribe
        :return: account subscribed
        :rtype: Account
        """
        pass

    @abstractmethod
    def get_contract(self):
        """Return contract for blockchain operations.
        This factory method return a prebuilt contract based on blockchain specifications.
        
        :param account: The account to subscribe
        :return: Account subscribed
        :rtype: Account
        """
        pass

    @abstractmethod
    def sign_transaction(self):
        """Sign transaction for blockchain using private key.
        
        :return: Signed transaction
        :rtype: eth_account.datastructures.SignedTransaction
        """
        pass

    @abstractmethod
    def send_transaction(self):
        """Commit signed transaction to blockchain.
        
        :return: Transaction hash
        :rtype: HexBytes
        """
        pass


class Contract(ABC):
    """Contract abstract class

    Specify all methods needed to interact with contracts.
    Use this class to create contract subtypes.

    Usage:
        class NFT(Contract):
            ....

    """
    def __init__(self, blockchain: Blockchain):
        self.blockchain = blockchain
        super().__init__()

    def __getattr__(self, name):
        """Called when an attribute lookup has not found the attribute in the usual places"""
        pass

    @abstractmethod
    @property
    def abi(root_path):
        """Return contract abi for contract
        
        :param root_path: Where is abi.json stored?
        :return: abi json 
        :rtype: dict
        """
        pass
