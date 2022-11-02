IMAGE_RESOURCE = 0
VIDEO_RESOURCE = 1

# Scheme constants
DEFAULT_RATE_MAX = 10
FIRST_MOVIE_YEAR_EVER = 1880

# Query constants
# Insert template fields are ordered based on model ordered dict field.
INSERT_MOVIE = """INSERT INTO movies(%s) VALUES(%s)"""
FETCH_MOVIE = """SELECT %s FROM movies"""
