import pydantic

from src.core.types import List
from src.sdk.harvest import Movie, Collector


# class MyMeta(Model):
#     """You can define your own data model here .
#     Write here any custom metadata model to distribute"""

#     title: str
#     address: str
#     ...


class File(Collector):
    def __str__(self):
        return "file"

    def __iter__(self):
        """Here could be implemented any logic to collect metadata."""

        # You can use pydantic helpers to handle any raw input
        # ref: https://docs.pydantic.dev/usage/models/#helper-functions
        source_file = "src/tests/_mock/files/dummy.json"
        return iter(pydantic.parse_file_as(List[Movie], source_file))
