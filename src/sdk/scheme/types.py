from pydantic.dataclasses import dataclass

Query = str


@dataclass
class Movie:
    movie_id: int
    # imdb code is adopted from IMB movies site to handle an alpha-numeric id
    imdb_code: str
    title: str
    group_name: str
    # creator key itself is a public key from blockchain network
    creator_key: str
    mpa_rating: str
    rating: float
    runtime: float
    release_year: int
    synopsis: str
    speech_language: str
    trailer_code: str
    date_uploaded: float


@dataclass
class MoviesResources:
    movie: Movie
    type: int
    route: str
