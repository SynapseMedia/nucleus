IMAGE_RESOURCE = 0
VIDEO_RESOURCE = 1

# Scheme constants
DEFAULT_RATE_MAX = 10
FIRST_MOVIE_YEAR_EVER = 1880

# Query constants
INSERT_MOVIE = """
INSERT INTO movies(
    imdb_code, 
    title, 
    creator_key,
    mpa_rating, 
    rating, 
    runtime, 
    release_year, 
    synopsis, 
    speech_language, 
    trailer_code, 
) VALUES(?,?,?,?,?,?,?,?,?,?)
"""

INSERT_RESOURCES = "INSERT INTO movies_resources() VALUES(?)"
