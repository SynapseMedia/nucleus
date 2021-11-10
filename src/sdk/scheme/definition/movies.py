"""
Scheme definition for movies used in watchit app
Exceptions:
    - If imdb_code cannot be found add your custom imdb_code ex: tt{movie_id}
    - If url its declared hash will be omitted or if hash its declared url will be omitted
"""
from datetime import date
from pathlib import Path
from cid import is_cid

import validators
from marshmallow import validates, fields, validate, ValidationError

from .generic import DataObjectScheme
from ...constants import (
    ALLOWED_STREAMING,
    DEFAULT_RATE_MAX,
    FIRST_MOVIE_YEAR_EVER,
    LONGEST_RUNTIME_MOVIE,
    SHORTEST_RUNTIME_MOVIE,
    DEFAULT_GENRES,
)


class MediaScheme(DataObjectScheme):
    """
    Generic abstract resource class definition
    :type route: Define how to reach the resource eg: cid | uri
    """

    route = fields.Str(required=True)  # Could be cid | uri
    index = fields.Str(required=False, default="index.m3u8")

    @validates("route")
    def validate_route(self, value):
        is_path = Path(value).exists()  # Check for existing file path
        is_url = validators.url(value)  # Check for valid url

        if not is_url and not is_path and not is_cid(value):
            raise ValidationError("Route must be a CID | URI | Path")


class VideoScheme(MediaScheme):
    """
    Video resource definition
    Implicit inherit `route`, `index` attrs from parent.
    :type quality: Screen quality definition for video
    :type type: Mechanism to stream video eg: hls | torrent
    """

    quality = fields.Str(required=True)  # Quality ex: 720p, 1080p..
    type = fields.Str(validate=validate.OneOf(ALLOWED_STREAMING))


class PostersScheme(DataObjectScheme):
    """
    Image collection with nested `MediaScheme`
    Each image must comply with `route` attr
    eg. {small:{route:...}, medium:{..}, large:{...}}
    """

    small = fields.Nested(MediaScheme)
    medium = fields.Nested(MediaScheme)
    large = fields.Nested(MediaScheme)


class MultiMediaScheme(DataObjectScheme):
    """
    Nested resource scheme
    """

    posters = fields.Nested(PostersScheme)
    videos = fields.List(fields.Nested(VideoScheme))


class MovieScheme(DataObjectScheme):
    title = fields.Str(validate=validate.Length(min=1))
    # if MIXED_RESOURCES=False then its needed for split dbs and keep groups for diff resources
    # Please use this name based on your resolver name defined in __str__ class method
    # ex: group_name = str(self) in resolver
    group_name = fields.Str(required=False)
    hash = fields.Str(require=False)
    # https://es.wikipedia.org/wiki/Internet_Movie_Database
    imdb_code = fields.Str(validate=validate.Regexp(r"^tt[0-9]{5,10}$"))
    price = fields.Float(validate=validate.Range(min=10000000000000000), dump_default=0, required=False)
    rating = fields.Float(validate=validate.Range(min=0, max=DEFAULT_RATE_MAX))
    year = fields.Int(validate=validate.Range(
        min=FIRST_MOVIE_YEAR_EVER, max=date.today().year + 1
    ))
    runtime = fields.Float(validate=validate.Range(
        min=SHORTEST_RUNTIME_MOVIE, max=LONGEST_RUNTIME_MOVIE
    ))
    genres = fields.List(
        fields.Str(), validate=validate.ContainsOnly(choices=DEFAULT_GENRES)
    )
    synopsis = fields.Str(required=True)
    trailer_code = fields.Str(missing=None)  # Youtube trailer code
    # https://meta.wikimedia.org/wiki/Template:List_of_language_names_ordered_by_code
    language = fields.Str(validate=validate.Length(min=2, max=10))
    # https://en.wikipedia.org/wiki/Motion_Picture_Association_film_rating_system
    mpa_rating = fields.Str(missing="PG")
    resource = fields.Nested(MultiMediaScheme)
    date_uploaded_unix = fields.Float(required=True)
