"""
Scheme definition for movies used in watchit app
Exceptions:
    - If imdb_code cannot be found add your custom imdb_code ex: tt{movie_id}
    - If url its declared hash will be omitted or if hash its declared url will be omitted
"""
import cid
import validators
from datetime import date
from marshmallow import Schema, validates, fields, validate, EXCLUDE, ValidationError

DEFAULT_RATE_MAX = 10
# Just in case according this
# https://en.wikipedia.org/wiki/1870s_in_film
# https://en.wikipedia.org/wiki/List_of_longest_films
# https://en.wikipedia.org/wiki/Fresh_Guacamole
FIRST_MOVIE_YEAR_EVER = 1880
LONGEST_RUNTIME_MOVIE = 51420
SHORTEST_RUNTIME_MOVIE = 1

ALLOWED_FORMATS = ['hls', 'torrent']
DEFAULT_GENRES = [
    'All', 'Action', 'Adventure', 'Animation', 'Biography',
    'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
    'Fantasy', 'Film-Noir', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'Romance',
    'Sci-Fi', 'Sport', 'Thriller', 'War', 'Western', 'News', 'Reality-TV', 'Talk-Show', 'Game-Show'
]


class GenericScheme(Schema):
    """
    Generic abstract resource class definition
    :type route: Define how to reach the resource eg: cid | uri
    :type index: This is the index file name definition
    """
    route = fields.Str(required=True)  # Could be cid | uri
    index = fields.Str()  # File index in directory
    abs = fields.Bool(default=False)

    @validates('route')
    def validate_route(self, value):
        if not cid.is_cid(value) and not validators.url(value):
            raise ValidationError('Route must be a CID or URI')


class VideoScheme(GenericScheme):
    """
    Video resource definition
    Implicit defined `route`, `index` attrs from parent.
    :type quality: Optional attribute if .m3u8 match in `index` or `uri`
    :type type: Mechanism to stream video eg: hls | torrent
    """
    quality = fields.Str(required=False)  # Quality ex: 720p, 1080p..
    type = fields.Str(validate=validate.OneOf(ALLOWED_FORMATS))


class ImageCollectionScheme(Schema):
    small = fields.Nested(GenericScheme)
    medium = fields.Nested(GenericScheme)
    large = fields.Nested(GenericScheme)


class ResourceScheme(Schema):
    """
    Nested resource scheme
    """
    images = fields.Nested(ImageCollectionScheme)
    videos = fields.List(fields.Nested(VideoScheme))


class MovieScheme(Schema):
    title = fields.Str(validate=validate.Length(min=1))
    # https://es.wikipedia.org/wiki/Internet_Movie_Database
    imdb_code = fields.Str(validate=validate.Regexp(r'^tt[0-9]{5,10}$'))
    rating = fields.Float(validate=validate.Range(min=0, max=DEFAULT_RATE_MAX))
    year = fields.Int(validate=validate.Range(min=FIRST_MOVIE_YEAR_EVER, max=date.today().year + 1))
    runtime = fields.Float(validate=validate.Range(min=SHORTEST_RUNTIME_MOVIE, max=LONGEST_RUNTIME_MOVIE))
    genres = fields.List(fields.Str(), validate=validate.ContainsOnly(choices=DEFAULT_GENRES))
    synopsis = fields.Str(required=True)
    # Public domain movie? Please help us to avoid piracy
    pdm = fields.Bool(default=False)
    trailer_code = fields.Str(missing=None)  # Youtube trailer code
    # https://meta.wikimedia.org/wiki/Template:List_of_language_names_ordered_by_code
    language = fields.Str(validate=validate.Length(min=2, max=10))
    # https://en.wikipedia.org/wiki/Motion_Picture_Association_film_rating_system
    mpa_rating = fields.Str(default='PG')
    resource = fields.Nested(ResourceScheme)
    date_uploaded_unix = fields.Int(required=True)
