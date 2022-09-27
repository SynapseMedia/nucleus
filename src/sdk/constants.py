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
VALIDATE_SSL = os.getenv("VALIDATE_SSL", "False") == "True"
ALLOWED_VIDEO_EXTENSIONS = {"mp4", "webm"}
ALLOWED_IMAGE_EXTENSIONS = {"jpeg", "png", "jpg", "gif"}

