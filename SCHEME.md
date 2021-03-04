### Scheme

The elaboration of the schema is quite simple, it consists in populate an array with dictionaries containing the
schematized metadata. Please check
our [example](https://github.com/ZorrillosDev/watchit-gateway/blob/master/resolvers/dummy/dummy.py).
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

#### VideoScheme

    url = fields.Url(relative=True)  # Remote|Local file
    cid = fields.Str()  # CID hash 
    index = fields.Str()  # File index in CID directory
    quality = fields.Str(required=True)  # 720p | 1080p | 2048p | 3D
    type = fields.Str() # torrent 

#### ImageScheme

    url = fields.Url(relative=True)  # Remote|Local file
    cid = fields.Str()  # CID hash
    index = fields.Str()  # File index in CID directory

#### MovieScheme

```
  title = fields.Str(validate=validate.Length(min=1))
  # Optional resource id to keep linked ex: origin?id=45
  resource_id = fields.Int(missing=0)
  # Where the data comes from?
  resource_name = fields.Str(validate=validate.Length(min=2))
  # https://es.wikipedia.org/wiki/Internet_Movie_Database
  imdb_code = fields.Str(validate=validate.Regexp(r'^tt[0-9]{5,10}$'))
  rating = fields.Float(validate=validate.Range(min=0, max=DEFAULT_RATE_MAX))
  year = fields.Int(validate=validate.Range(min=FIRST_MOVIE_YEAR_EVER, max=date.today().year + 1))
  runtime = fields.Float(validate=validate.Range(min=SHORTEST_RUNTIME_MOVIE, max=LONGEST_RUNTIME_MOVIE))
  genres = fields.List(fields.Str(), validate=validate.ContainsOnly(choices=DEFAULT_GENRES))
  synopsis = fields.Str(required=True)
  # Public domain movie? Please help us to avoid piracy
  pdm = fields.Bool(default=True)
  trailer_code = fields.Str(missing=None)  # Youtube trailer code
  # https://meta.wikimedia.org/wiki/Template:List_of_language_names_ordered_by_code
  language = fields.Str(validate=validate.Length(min=2, max=10))
  # https://en.wikipedia.org/wiki/Motion_Picture_Association_film_rating_system
  mpa_rating = fields.Str(default='PG')
  # This uri links should be declared to IPFS ingestion
  small_image = fields.Nested(ImageScheme)
  medium_image = fields.Nested(ImageScheme)
  large_image = fields.Nested(ImageScheme)
  resource = fields.List(fields.Nested(VideoScheme))
  date_uploaded_unix = fields.Int(required=True)
```
