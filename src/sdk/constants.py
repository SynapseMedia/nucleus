import os
from datetime import date

# Setup mongo local temp cache
MONGO_HOST, MONGO_PORT = ("mongo", "27017")
DB_DATE_VERSION = date.today().strftime("%Y%m%d")
ROOT_PROJECT = os.getenv("PROJECT_ROOT")
REGEN_MOVIES = os.getenv("REGEN_MOVIES", "False") == "True"

# Fetching constants
VALIDATE_SSL = os.getenv("VALIDATE_SSL", "False") == "True"
RAW_PATH = os.getenv("RAW_DIRECTORY")
PROD_PATH = os.getenv("PROD_DIRECTORY")

# Pinata settings
PINATA_PSA = os.getenv("PINATA_PSA")
PINATA_API_JWT = os.getenv("PINATA_API_JWT")
PINATA_API_KEY = os.getenv("PINATA_API_KEY")
PINATA_SERVICE = os.getenv("PINATA_SERVICE", "pinata")
PINATA_ENDPOINT = os.getenv("PINATA_ENDPOINT", "https://api.pinata.cloud")
PINATA_API_SECRET = os.getenv("PINATA_API_SECRET")
# Background process for pinata pinning?
PINATA_PIN_BACKGROUND = os.getenv("PINATA_PIN_BACKGROUND", "False") == "True"

# Http settings
NODE_URI = os.getenv("NODE_URI")
API_VERSION = os.getenv("API_VERSION")

# Transcode constants
OVERWRITE_TRANSCODE_OUTPUT = os.getenv("OVERWRITE_TRANSCODE_OUTPUT", "False") == "True"
RECURSIVE_SLEEP_REQUEST = 5
MAX_MUXING_QUEUE_SIZE = 9999
MAX_FAIL_RETRY = 3
HLS_TIME = 5
HLS_LIST_SIZE = 10
HLS_FORMAT = "hls"
DASH_FORMAT = "dash"
DEFAULT_NEW_FILENAME = "index.m3u8"
HLS_NEW_FILENAME = "index.m3u8"
DASH_NEW_FILENAME = "index.mpd"

# Ingest constants
IPFS_NODE = os.getenv("IPFS_NODE")
IPFS_CONTAINER = os.getenv("IPFS_CONTAINER")
IPFS_NODE_GATEWAY_PORT = os.getenv("IPFS_NODE_GATEWAY_PORT")
FLUSH_CACHE_IPFS = os.getenv("FLUSH_CACHE_IPFS", "False") == "True"
TIMEOUT_REQUEST = 120 * 60

# Export constants
REGEN_ORBITDB = os.environ.get("REGEN_ORBITDB", "False") == "True"
MIXED_RESOURCES = os.environ.get("MIXED_RESOURCES", "False") == "True"

# Web3 constants
KOVAN_PROVIDER = os.getenv("KOVAN_PROVIDER", "")
KOVAN_ALCHEMY_API_KEY = os.getenv("KOVAN_ALCHEMY_API_KEY", "")
KOVAN_CONTRACT_NFT = os.getenv("KOVAN_CONTRACT_NFT", "")
RINKEBY_PROVIDER = os.getenv("RINKEBY_PROVIDER", "")
RINKEBY_ALCHEMY_API_KEY = os.getenv("RINKEBY_ALCHEMY_API_KEY", "")
RINKEBY_CONTRACT_NFT = os.getenv("RINKEBY_CONTRACT_NFT", "")
WALLET_KEY = os.getenv("WALLET_KEY")
WALLET_PUBLIC_KEY = os.getenv("WALLET_PUBLIC_KEY")

# Scheme constants
DEFAULT_RATE_MAX = 10
# Just in case according this
# https://en.wikipedia.org/wiki/1870s_in_film
# https://en.wikipedia.org/wiki/List_of_longest_films
# https://en.wikipedia.org/wiki/Fresh_Guacamole
FIRST_MOVIE_YEAR_EVER = 1880
LONGEST_RUNTIME_MOVIE = 51420
SHORTEST_RUNTIME_MOVIE = 1

DEFAULT_GENRES = [
    "All",
    "Action",
    "Adventure",
    "Animation",
    "Biography",
    "Comedy",
    "Crime",
    "Documentary",
    "Drama",
    "Family",
    "Fantasy",
    "Film-Noir",
    "History",
    "Horror",
    "Music",
    "Musical",
    "Mystery",
    "Romance",
    "Sci-Fi",
    "Sport",
    "Thriller",
    "War",
    "Western",
    "News",
    "Reality-TV",
    "Talk-Show",
    "Game-Show",
]
