# Scheme constants
from nucleus.core.constants import ROOT_DIR

# Runtime directories
COLLECTORS_PATH = f'{ROOT_DIR}/collectors/'
MODELS_PATH = './.models/'

# Query constants
# Insert template fields are ordered based on model ordered dict field.
MIGRATE = """CREATE TABLE IF NOT EXISTS %s(m %s);"""
INSERT = """INSERT INTO %s VALUES(?)"""
FETCH = """SELECT m FROM %s"""
