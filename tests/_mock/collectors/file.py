import json

from nucleus.core.types import JSON
from nucleus.sdk.harvest import Collector


class File(Collector):
    """File implements Collector interface"""

    def __iter__(self):
        """Here could be implemented any logic to collect metadata."""

        source_file = 'tests/_mock/files/dummy.json'
        with open(source_file) as file:
            # read movies from json file
            for data in json.load(file):
                yield JSON(data)
