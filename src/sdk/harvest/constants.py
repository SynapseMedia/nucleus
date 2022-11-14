# Scheme constants
DEFAULT_RATE_MAX = 10
FIRST_MOVIE_YEAR_EVER = 1880

# Query constants
# Insert template fields are ordered based on model ordered dict field.
INSERT_MOVIE = """INSERT INTO movies(m) VALUES(?)"""
FETCH_MOVIE = """SELECT m FROM movies"""
