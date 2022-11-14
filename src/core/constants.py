import os

# Http settings
PROJECT_ROOT = os.getenv("PROJECT_ROOT")
VALIDATE_SSL = os.getenv("VALIDATE_SSL", "False") == "True"
