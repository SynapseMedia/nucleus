
import os
# Edge cache settings
DEFAULT_EDGE_SERVICE = os.getenv("DEFAULT_EDGE_SERVICE", "pinata")

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
VALIDATE_SSL = os.getenv("VALIDATE_SSL", "False") == "True"
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "/multimedia/tmp")
ALLOWED_VIDEO_EXTENSIONS = {"mp4", "webm"}
ALLOWED_IMAGE_EXTENSIONS = {"jpeg", "png", "jpg", "gif"}

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
