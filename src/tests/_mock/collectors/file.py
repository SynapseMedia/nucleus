import json


class File:
    def __str__(self):
        return "file"

    def __iter__(self):
        """Here could be implemented any logic to collect metadata."""
        source_file = "src/tests/_mock/files/dummy.json"
        with open(source_file) as file:
            # read movies from json file
            meta = json.load(file)

            for raw in meta:
                yield raw
