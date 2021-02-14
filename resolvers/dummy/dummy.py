class Dummy:

    def __str__(self) -> str:
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
            "small_cover_image": "https://static.hollywoodreporter.com/sites/default/files/2018/09/coming_to_netflix_in_october_2018-_the_seven_deadly_sins-_revival_of_the_commandments-publicity_-production_still-_h_2018-768x433.jpg",
            "medium_cover_image": "https://static.hollywoodreporter.com/sites/default/files/2018/09/coming_to_netflix_in_october_2018-_the_seven_deadly_sins-_revival_of_the_commandments-publicity_-production_still-_h_2018-768x433.jpg",
            "large_cover_image": "https://static.hollywoodreporter.com/sites/default/files/2018/09/coming_to_netflix_in_october_2018-_the_seven_deadly_sins-_revival_of_the_commandments-publicity_-production_still-_h_2018-768x433.jpg",
            "date_uploaded_unix": 1446321498,
            "resource": [
                {
                    "hash": "QmVuR5s1enhtAK5ipvLNiqgSz8CecCkPL8GumrBE3e53gg",
                    "quality": "720p",
                    "index": "index.m3u8",
                    "type": "hls"
                }
            ]
        }], many=True)

    def __call__(self, scheme) -> list:
        """
        Returned meta should be valid scheme
        """
        yield Dummy.data(scheme)
