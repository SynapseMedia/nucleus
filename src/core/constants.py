import os
import pathlib

# Http settings
ROOT_DIR = pathlib.Path().resolve()  # relative root path
VALIDATE_SSL = os.getenv("VALIDATE_SSL", "False") == "True"
