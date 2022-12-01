# Convention for importing types
class Dummy:
    def __str__(self):
        return "dummy"

    def __iter__(self):
        """Here could be implemented any logic to collect metadata."""
        
        dummy_data = [{
            "title": "A Fork in the Road",
            "synopsis": "Baby loves have fun",
            "imdb_code": "wtt00000000",
            "genres": ["Action", "Comedy", "Crime"],
            "creator_key": "0xee99ceff640d37edd9cac8c7cff4ed4cd609f435",
            "speech_language": "en",
            "release_year": 2010,
            "runtime": 105.0,
            "mpa_rating": "PG",
            "rating": 6.0,
        }]
        
        for raw in dummy_data:
            yield raw
