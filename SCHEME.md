### Scheme

We need predefined scheme definition to ensure the integrity of the data that is later consumed by the [dapp](https://github.com/ZorrillosDev/watchit-desktop).
The process to elaborate the schema is quite simple, basically consists in populate an array with dictionaries containing the
schematized metadata as shown in this [example](https://github.com/ZorrillosDev/watchit-gateway/blob/master/resolvers/dummy/dummy.py).
See [scheme definition](https://github.com/ZorrillosDev/watchit-gateway/blob/master/src/core/scheme/definition.py).

Some env vars used below to define schemas:

```
FIRST_MOVIE_YEAR_EVER = 1880
LONGEST_RUNTIME_MOVIE = 51420 # Minutes
SHORTEST_RUNTIME_MOVIE = 1 # Minutes
DEFAULT_GENRES = 'All' | 'Action' | 'Adventure' | 'Animation' | 
    'Biography' | 'Comedy' | 'Crime' | 'Documentary' | 'Drama' | 'Family' |
    'Fantasy' | 'Film-Noir' | 'Game-Show' | 'History' | 'Horror' | 'Music' | 'Musical' |
    'Mystery' | 'News' | 'Romance' | 'Reality-TV' | 'Sci-Fi' | 'Sport' | 'Talk-Show' | 'Thriller' | 
    'War' | 'Western'  
```

### GenericScheme(Schema):

    """
    Generic abstract resource class definition
    :type route: Define how to reach the resource eg: cid | uri
    :type index: This is the index file name definition
    :type abs: Bool flag to absolute or not `route` defined
    """
    route = fields.Str(required=True)  # Could be cid | uri
    index = fields.Str()  # File index in directory
    abs = fields.Bool(default=False)

#### VideoScheme(GenericScheme)
    """
    Video resource definition 
    Implicit defined `route`, `index` attrs from parent.
    :type quality: Screen quality definition for video
    :type type: Mechanism to stream video eg: hls | torrent
    """
    quality = fields.Str(required=False)  # Quality ex: 720p, 1080p..
    type = fields.Str(validate=validate.OneOf(ALLOWED_FORMATS))

### ImageCollectionScheme:

    small = fields.Nested(GenericScheme)
    medium = fields.Nested(GenericScheme)
    large = fields.Nested(GenericScheme)

### ResourceScheme

    images = fields.Nested(ImageCollectionScheme)
    videos = fields.List(fields.Nested(VideoScheme))

#### MovieScheme

    title = fields.Str(validate=validate.Length(min=1))
    # https://es.wikipedia.org/wiki/Internet_Movie_Database
    imdb_code = fields.Str(validate=validate.Regexp(r'^tt[0-9]{5,10}$'))
    rating = fields.Float(validate=validate.Range(min=0, max=DEFAULT_RATE_MAX))
    year = fields.Int(validate=validate.Range(min=FIRST_MOVIE_YEAR_EVER, max=date.today().year + 1))
    runtime = fields.Float(validate=validate.Range(min=SHORTEST_RUNTIME_MOVIE, max=LONGEST_RUNTIME_MOVIE))
    genres = fields.List(fields.Str(), validate=validate.ContainsOnly(choices=DEFAULT_GENRES))
    synopsis = fields.Str(required=True)
    # Public domain movie? Please help us to avoid piracy
    pdm = fields.Bool(default=False)
    trailer_code = fields.Str(missing=None)  # Youtube trailer code
    # https://meta.wikimedia.org/wiki/Template:List_of_language_names_ordered_by_code
    language = fields.Str(validate=validate.Length(min=2, max=10))
    # https://en.wikipedia.org/wiki/Motion_Picture_Association_film_rating_system
    mpa_rating = fields.Str(default='PG')
    resource = fields.Nested(ResourceScheme)
    date_uploaded_unix = fields.Int(required=True)
