import json

from nucleus.sdk.harvest import Collector

# class MyMeta(Meta):
#     """You can define your own data model here .
#     Write here any custom metadata model to distribute"""

#     title: str
#     address: str
#     ...


class File(Collector):
    """File implements Collector interface"""

    def __iter__(self):
        """Here could be implemented any logic to collect metadata."""

        source_file = 'nucleus/tests/_mock/files/dummy.json'
        with open(source_file) as file:
            # read movies from json file
            yield from json.load(file)
