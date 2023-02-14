# Scheme constants
from src.core.constants import ROOT_DIR

# Query constants
# Insert template fields are ordered based on model ordered dict field.
MIGRATE = """CREATE TABLE IF NOT EXISTS %ss(m %s);"""
INSERT = """INSERT INTO %ss(m) VALUES(?)"""
FETCH = """SELECT m FROM %ss"""

# Runtime directories
COLLECTORS_PATH = f"{ROOT_DIR}/collectors/"

