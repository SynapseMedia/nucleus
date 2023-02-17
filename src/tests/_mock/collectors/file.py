import json

from src.sdk.harvest import Collector, Collection, Image
from src.tests._mock.models import Movie

# class MyMeta(Meta):
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

        source_file = "src/tests/_mock/files/dummy.json"
        with open(source_file) as file:
            # read movies from json file
            for raw in json.load(file):
                raw_movie = raw.get("metadata")
                raw_media = raw.get("media")

                yield Collection(
                    metadata=Movie(**raw_movie),
                    media=[Image(**m) for m in raw_media],
                )
