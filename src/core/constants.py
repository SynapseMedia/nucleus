import os

# Http settings
VALIDATE_SSL = os.getenv("VALIDATE_SSL", "False") == "True"

# Runtime directories
PROJECT_ROOT = os.getenv("PROJECT_ROOT")
RUNTIME_DIRECTORY = os.getenv("RUNTIME_DIRECTORY")
RAW_PATH = os.getenv("RAW_DIRECTORY")
PROD_PATH = os.getenv("PROD_DIRECTORY")
