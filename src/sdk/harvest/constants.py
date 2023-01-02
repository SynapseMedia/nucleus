# Scheme constants
import os

from src.core.constants import ROOT_DIR

DEFAULT_RATE_MAX = 10
FIRST_MOVIE_YEAR_EVER = 1880

# Query constants
# Insert template fields are ordered based on model ordered dict field.
INSERT_MOVIE = """INSERT INTO movies(m) VALUES(?)"""
FETCH_MOVIE = """SELECT m FROM movies"""

# Runtime directories
COLLECTORS_PATH = f"{ROOT_DIR}/collectors/"
RUNTIME_DIRECTORY = os.getenv("RUNTIME_DIRECTORY")
RAW_PATH = os.getenv("RAW_DIRECTORY")
PROD_PATH = os.getenv("PROD_DIRECTORY")
