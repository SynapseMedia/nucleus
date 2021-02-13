class Dummy:

    def __str__(self):
        return 'Test'

    @staticmethod
    def data(scheme) -> list:
        """
        Process your data and populate scheme struct
        src/core/scheme/definition.py
        """
        return scheme.validator.check([{
            "resource_id": 85,
            "imdb_code": "tt00000",
            "title": "A Fork in the Road",
            "year": 2010, "rating": 6, "runtime": 105,
            "genres": ["Action", "Comedy", "Crime"],
            "synopsis": "Baby loves have fun",
            "trailer_code": "uIrQ9535RFo",
            "language": "en",
            "small_cover_image": "https://happy.com/legal/movies/baby_test_movie.jpg",
            "medium_cover_image": "https://happy.com/legal/movies/baby_test_movie.jpg",
            "large_cover_image": "https://happy.com/legal/movies/baby_test_movie.jpg",
            "date_uploaded_unix": 1446321498,
            "resource": [
                {
                    "url": "https://happy.com/legal/movies/baby_test_movie/torrent.file",
                    "hash": "778EF443F532DCB6F0383310E2E4935C76BADC9F",
                    "quality": "720p",
                    "type": "torrent"
                }
            ]
        }], many=True)

    def __call__(self, scheme) -> list:
        """
        Returned meta should be valid scheme
        """
        return Dummy.data(scheme)
