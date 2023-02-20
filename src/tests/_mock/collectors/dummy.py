from src.sdk.harvest import Collector, Collection, Image
from src.tests._mock.models import Movie


class Dummy(Collector):
    def __str__(self):
        return "dummy"

    def __iter__(self):
        """Here could be implemented any logic to collect metadata."""

        dummy_data = [{"metadata": {"title": "A Fork in the Road",
                                    "imdb_code": "wtt00000000",
                                    "creator_key": "0xee99ceff640d37edd9cac8c7cff4ed4cd609f435",
                                    "mpa_rating": "PG",
                                    "rating": 6.0,
                                    "runtime": 105.0,
                                    "synopsis": "Baby loves have fun",
                                    "release_year": 2010,
                                    "genres": ["Action",
                                                  "Comedy",
                                                  "Crime"],
                                    "speech_language": "en",
                                    "publish_date": 1669911990.9270618,
                                    },
                       "media": [{"route": "src/tests/_mock/files/watchit.png",
                                  "type": "image",
                                  }],
                       }]

        for raw in dummy_data:
            # how should we handle metadata?
            raw_movie = raw.get("metadata")
            raw_media = raw.get("media", [])

            yield Collection(
                metadata=Movie.parse_obj(raw_movie),
                media=[Image.parse_obj(m) for m in raw_media],
            )
