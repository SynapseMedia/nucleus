"""
Scheme definition for movies. 
Each scheme here defined help us to keep a standard for runtime processing of movies. 
All processed data is later used in the creation of standard metadata (ERC-1155, ..); 
In addition, this metadata is used for marshalling process.
"""
import re
import pydantic
import datetime

# Convention for importing constants
from src.sdk.constants import DEFAULT_RATE_MAX, FIRST_MOVIE_YEAR_EVER


@pydantic.dataclasses.dataclass
class MoviesResources:
    route: str
    type: int

    # TODO validate type and route


@pydantic.dataclasses.dataclass
class Movies:
    """Movies define needed fields for standard movie schema."""

    title: str
    # imdb code is adopted from IMB movies site to handle an alpha-numeric id
    # https://es.wikipedia.org/wiki/Internet_Movie_Database
    imdb_code: str
    # creator key itself is a public key from blockchain network
    creator_key: str
    # # https://en.wikipedia.org/wiki/Motion_Picture_Association_film_rating_system
    mpa_rating: str
    # price could be set as initial price for movie.
    # This price will be will be used for "monetization" purpose
    price: float
    rating: float
    runtime: float
    release_year: int
    synopsis: str
    # https://meta.wikimedia.org/wiki/Template:List_of_language_names_ordered_by_code
    speech_language: str
    trailer_link: str
    date_uploaded: float
    genres: list[str]

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

    @pydantic.validator("price")
    def min_price_value(cls, v: float):
        assert v >= 0, (
            """
            Invalid price value: %s.
            Price should be greater than zero.
            """
            % v
        )
        return v

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
