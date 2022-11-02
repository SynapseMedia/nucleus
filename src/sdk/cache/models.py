import re
import time
import json
import pydantic
import datetime
import validators  # type: ignore
import cid  # type: ignore
import pathlib

# Convention for importing types/constants
# Convention for relative internal import
from src.core.types import Optional, List
from .types import CoreModel

# Exception for relative internal importing
from .constants import (
    DEFAULT_RATE_MAX,
    FIRST_MOVIE_YEAR_EVER,
    VIDEO_RESOURCE,
    IMAGE_RESOURCE,
)


class Media(pydantic.BaseModel):
    """Media define needed field for the multimedia assets schema."""

    route: str
    type: int

    @pydantic.validator("type")
    def valid_type(cls, v: int):
        if v not in [VIDEO_RESOURCE, IMAGE_RESOURCE]:
            raise ValueError(
                """
                Invalid resource type.
                Allowed types:
                    - VIDEO = 1
                    - IMAGE = 0
                """
            )
        return v

    @pydantic.validator("route")
    def valid_route(cls, v: str):
        is_path = pathlib.Path(v).exists()  # type: ignore
        is_url = bool(validators.url(v))  # type: ignore
        is_cid = bool(cid.is_cid(v))  # type: ignore

        if not is_url and not is_path and not is_cid:
            raise ValueError("Route must be a CID | URI | Path")

        return v


class Movie(CoreModel):
    """Movies define needed fields for standard movie schema."""

    title: str
    # imdb code is adopted from IMB movies site to handle an alpha-numeric id
    # https://es.wikipedia.org/wiki/Internet_Movie_Database
    imdb_code: str
    # creator key itself is a public key from blockchain network
    creator_key: str
    # # https://en.wikipedia.org/wiki/Motion_Picture_Association_film_rating_system
    mpa_rating: str
    rating: float
    runtime: float
    synopsis: str
    release_year: int
    # https://meta.wikimedia.org/wiki/Template:List_of_language_names_ordered_by_code
    genres: list[str]
    speech_language: str
    publish_date: Optional[float] = None
    trailer_link: Optional[str] = None
    # Add movie multimedia resources
    resources: list[Media] = []

    @pydantic.validator("resources", pre=True)
    def serialize_resources_pre(cls, v: str):
        if type(v) == str:
            return json.loads(v)
        return v

    @pydantic.validator("genres", pre=True)
    def serialize_genres_pre(cls, v: str):
        if type(v) == str:
            return v.split(",")
        return v

    @pydantic.validator("resources")
    def serialize_resources(cls, v: List[Media]):
        return json.dumps(list(map(lambda x: x.dict(), v)))

    @pydantic.validator("genres")
    def serialize_genres(cls, v: List[str]):
        return ", ".join(v)

    @pydantic.validator("publish_date", pre=True, always=True)
    def publish_date_default(cls, v: float):
        return v or time.time()

    @pydantic.validator("imdb_code")
    def imdb_valid_format(cls, v: str):
        pattern = re.compile(r"^w?t[a-zA-Z0-9]{8,32}$")
        if not re.fullmatch(pattern, v):
            raise ValueError(
                """
                Invalid imdb code pattern: %s.
                Pattern must match: r"^w?t[a-zA-Z0-9]{8,32}$"       
                """
                % v
            )
        return v

    @pydantic.validator("rating")
    def rating_range(cls, v: float):
        if v < 0 or v > DEFAULT_RATE_MAX:
            raise ValueError(
                """
                Invalid rating range: %s.
                Min rating should be >= 0 and <= 10
                """
                % v
            )
        return v

    @pydantic.validator("mpa_rating", pre=True, always=True)
    def mpa_rating_default(cls, v: str):
        return v or "PG"

    @pydantic.validator("release_year")
    def year_range(cls, v: float):
        # https://en.wikipedia.org/wiki/1870s_in_film
        if v < FIRST_MOVIE_YEAR_EVER or v > datetime.date.today().year + 1:
            raise ValueError(
                """
                Invalid movie release year.
                Year should be greater than 1880 (date of first created movie)
                and less than the current year.
                """
            )
        return v

    @pydantic.validator("genres", each_item=True)
    def valid_genres(cls, v: str):
        if v == "" or len(v) < 3:
            raise ValueError(
                """
                Invalid genres for movie.
                Genres should be not empty and contain at least 3 characters.
                """
            )
        return v