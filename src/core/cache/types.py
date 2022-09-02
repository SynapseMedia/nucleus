from abc import ABCMeta
from pydantic import BaseModel

Query = str


class Model(BaseModel, metaclass=ABCMeta):
    def query(self):
        ...

    def get(self):
        ...

    def fetch(self):
        ...

    def create(self):
        ...

    def update(self):
        ...

    def delete(self):
        ...


# @dataclass
# class Movie:
#     movie_id INTEGER PRIMARY KEY,
#     -- imdb code is adopted from IMB movies site to handle an alpha-numeric id
#     imdb_code TEXT KEY DESC,
#     title TEXT KEY DESC,
#     group_name TEXT KEY,
#     -- creator key itself is a public key from blockchain network
#     creator_key TEXT,
#     mpa_rating TEXT,
#     rating REAL,
#     runtime REAL,
#     release_year INTEGER,
#     synopsis TEXT,
#     speech_language TEXT,
#     trailer_code TEXT,
#     date_uploaded REAL
