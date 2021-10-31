import os

# Fetching constants
VALIDATE_SSL = os.getenv("VALIDATE_SSL", "False") == "True"
RAW_PATH = os.getenv("RAW_DIRECTORY")
PROD_PATH = os.getenv("PROD_DIRECTORY")

# Transcode constants
OVERWRITE_TRANSCODE_OUTPUT = os.getenv("OVERWRITE_TRANSCODE_OUTPUT", "False") == "True"
MAX_FAIL_RETRY = 3
RECURSIVE_SLEEP_REQUEST = 5
DEFAULT_FORMAT = "hls"
DEFAULT_HLS_TIME = 5
DEFAULT_HLS_FORMAT = "m3u8"
DEFAULT_NEW_FILENAME = "index.m3u8"

# Ingest constants
FLUSH_CACHE_IPFS = os.getenv("FLUSH_CACHE_IPFS", "False") == "True"
AUTO_PIN_FILES = os.getenv("AUTO_PIN_FILES", "False") == "True"
TIMEOUT_REQUEST = 30 * 60

# Export constants
REGEN_ORBITDB = os.environ.get("REGEN_ORBITDB", "False") == "True"
MIXED_RESOURCES = os.environ.get("MIXED_RESOURCES", "False") == "True"

# Web3 constants
KOVAN_PROVIDER = os.getenv("KOVAN_PROVIDER", "")
KOVAN_ALCHEMY_API_KEY = os.getenv("KOVAN_ALCHEMY_API_KEY", "")
KOVAN_CONTRACT_NFT = os.getenv("KOVAN_CONTRACT_NFT", "")
WALLET_KEY = os.getenv("WALLET_KEY")
