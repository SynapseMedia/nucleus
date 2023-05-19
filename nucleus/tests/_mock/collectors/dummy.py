from nucleus.sdk.harvest import Collector


class Dummy(Collector):
    """Dummy implements Collector"""

    def __iter__(self):
        """Here could be implemented any logic to collect metadata."""

        dummy_data = [
            {
                'metadata': {
                    'name': 'A Fork in the Road',
                    'imdb_code': 'wtt00000000',
                    'creator_key': '0xee99ceff640d37edd9cac8c7cff4ed4cd609f435',
                    'mpa_rating': 'PG',
                    'rating': 6.0,
                    'runtime': 105.0,
                    'desc': 'Baby loves have fun',
                    'release_year': 2010,
                    'genres': ['Action', 'Comedy', 'Crime'],
                    'speech_language': 'en',
                    'publish_date': 1669911990.9270618,
                },
                'media': [{'path': 'nucleus/tests/_mock/files/watchit.png'}],
            }
        ]

        yield from dummy_data
