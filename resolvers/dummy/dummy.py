import json
import os
from src.core import logger


class Dummy:
    def __init__(self, scheme):
        """
        Initialize resolver with scheme module
        :param scheme: Scheme define method to validate and clean scheme
        """
        self.scheme = scheme
        pass

    def __str__(self):
        return 'Test'

    def data(self):
        return [dict(
            resource_id=85,
            imdb_code="tt00000",
            title="A Fork in the Road",
            year=2010, rating=6, runtime=105,
            genres=["Action", "Comedy", "Crime"],
            synopsis="Baby loves have fun",
            trailer_code="uIrQ9535RFo",
            language="en",
            small_cover_image="https://happy/legal/movies/baby_test_movie/small-cover.jpg",
            medium_cover_image="https://happy/legal/movies/baby_test_movie/medium-cover.jpg",
            large_cover_image="https://happy/legal/movies/baby_test_movie/large-cover.jpg",
            date_uploaded_unix=1446321498,
            torrents=[
                {
                    "url": "https://happy/legal/movies/baby_test_movie/torrent.file",
                    "hash": "778EF443F532DCB6F0383310E2E4935C76BADC9F",
                    "quality": "720p"
                }
            ]
        )]

    def __call__(self, *args, **kwargs):
        """
        Return should be valid scheme
        please check code/scheme/definition.py
        """
        self.scheme.validator.check(self.data())
        return self.data()
