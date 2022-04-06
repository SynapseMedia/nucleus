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
        yield [{
            "imdb_code": "wtt00000000",
            "title": "A Fork in the Road",
            "year": 2010,
            "rating": 6,
            "creator": "0xee99ceff640d37edd9cac8c7cff4ed4cd609f435",
            "runtime": 105,
            # if MIXED_RESOURCES=False then its needed for split dbs and keep groups for diff resources
            # Please use this name based on your resolver name defined in __str__ class method
            # ex: group_name = str(self) in resolver
            "group_name": str(self),
            "genres": ["Action", "Comedy", "Crime"],
            "synopsis": "Baby loves have fun",
            "trailer_code": "uIrQ9535RFo",
            "language": "en",
            "date_uploaded_unix": 1446321498,
            "resource": {
                "image": {
                    "route": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/images/BigBuckBunny.jpg"
                },
                "video": {
                    "route": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
                }

            }}]
