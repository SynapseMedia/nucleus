# Scheme constants
from src.core.constants import ROOT_DIR

# Query constants
# Insert template fields are ordered based on model ordered dict field.
MIGRATE = """CREATE TABLE IF NOT EXISTS %s(m %s);"""
INSERT = """INSERT INTO %s(m) VALUES(?)"""
FETCH = """SELECT m FROM %s"""

# Runtime directories
COLLECTORS_PATH = f"{ROOT_DIR}/collectors/"
