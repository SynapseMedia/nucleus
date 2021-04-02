class Dummy:

    def __str__(self) -> str:
        return 'dummy'

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
            "year": 2010, "rating": 6,
            "runtime": 105,
            # if MIXED_RESOURCES=False then its needed for split dbs and keep groups for diff resources
            # Please use this name based on your resolver name defined in __str__ class method
            # ex: link_name = str(self) in resolver
            "link_name": str(self),
            "genres": ["Action", "Comedy", "Crime"],
            "synopsis": "Baby loves have fun",
            "trailer_code": "uIrQ9535RFo",
            "language": "en",
            "date_uploaded_unix": 1446321498,
            "resource": {
                "images": {
                    "small": {
                        "route": "https://images-na.ssl-images-amazon.com/images/I/71-i1berMyL._AC_SL1001_.jpg"
                    },
                    "medium": {
                        "route": "https://images-na.ssl-images-amazon.com/images/I/71-i1berMyL._AC_SL1001_.jpg"
                    },
                    "large": {
                        "route": "https://images-na.ssl-images-amazon.com/images/I/71-i1berMyL._AC_SL1001_.jpg"
                    },
                },
                "videos": [
                    {
                        "route": "QmVuR5s1enhtAK5ipvLNiqgSz8CecCkPL8GumrBE3e53gg",
                        "quality": "720p",
                        "index": "index.m3u8",
                        "type": "hls"
                    }
                ]
            }}])
