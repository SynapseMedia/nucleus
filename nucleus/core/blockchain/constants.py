import os

from nucleus.core.constants import ROOT_DIR

# Web3 constants

GWEI = 1000000000
NFT_ABI_PATH = f'{ROOT_DIR}/abi/WNFT.json'
WALLET_KEY = os.getenv('WALLET_KEY', '')
WALLET_PUBLIC_KEY = os.getenv('WALLET_PUBLIC_KEY')

GOERLI_PROVIDER = os.getenv('GOERLI_PROVIDER', '')
GOERLI_ALCHEMY_API_KEY = os.getenv('GOERLI_ALCHEMY_API_KEY', '')
GOERLI_CONTRACT_NFT = os.getenv('GOERLI_CONTRACT_NFT', '')
