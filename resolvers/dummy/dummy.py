class Dummy:

    def __str__(self) -> str:
        return 'Test'

    def __call__(self, scheme):
        """
        Returned meta should be valid scheme
        Process your data and populate scheme struct
        src/core/scheme/definition.py

        :param scheme: Scheme object
        :returns: Scheme valid object list ex: {movie1, movie2}
        :rtype Generator
        """
        yield scheme.validator.check([{
            "imdb_code": "tt00000",
            "title": "A Fork in the Road",
            "year": 2010, "rating": 6, "runtime": 105,
            "genres": ["Action", "Comedy", "Crime"],
            "synopsis": "Baby loves have fun",
            "trailer_code": "uIrQ9535RFo",
            "language": "en",
            "date_uploaded_unix": 1446321498,
            "resource": {
                "images": {
                    "small_image": {
                        "route": "https://images-na.ssl-images-amazon.com/images/I/71-i1berMyL._AC_SL1001_.jpg"
                    },
                    "medium_image": {
                        "route": "https://images-na.ssl-images-amazon.com/images/I/71-i1berMyL._AC_SL1001_.jpg"
                    },
                    "large_image": {
                        "route": "https://images-na.ssl-images-amazon.com/images/I/71-i1berMyL._AC_SL1001_.jpg"
                    },
                },
                "video": [
                    {
                        "route": "QmVuR5s1enhtAK5ipvLNiqgSz8CecCkPL8GumrBE3e53gg",
                        "quality": "720p",
                        "index": "index.m3u8",
                        "type": "hls"
                    }
                ]
            }}])
