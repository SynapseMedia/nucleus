# Watchit Gateway

[![Gitter](https://badges.gitter.im/watchit-app/community.svg)](https://gitter.im/watchit-app/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

## Getting started

* [Spawn go-ipfs node with docker](https://mrh.io/ipfs_docker/).
* [How to spawn an IPFS node in Node.js](https://mrh.io/2018-01-24-pushing-limits-ipfs-orbitdb/).
* For private networks [How to spawn an IPFS private node and generate swarm key](https://mrh.io/ipfs-private-networks/)
  .

## Quick summary

The watchit gateway is an interface or micro framework for the migration of content to IPFS and the distribution of
metadata through [OrbitDB](https://orbitdb.org/).

Watchit gateway adds migrated data to the metastore (orbitdb) which is distributed in a predefined scheme definition to
ensure the integrity of the data that is later consumed by the [dapp](https://github.com/ZorrillosDev/watchit-desktop).
Watchit gateway provides simple tools for the generation and fetching of content.

## Tools

### Resolvers

"A _resolver_ is a set of instructions, expressed as a Python class. A _gateway_ will execute a resolver to fetch
content from various sources." - @aphelionz

Resolvers implement the logic necessary for fetch, preprocessing, cleaning and schematization of data from any available
resource. Based on the following class abstraction we can see the methods required for the development of a resolver:

~~~~
Define your resolvers modules below.
Ex: Each resolver must implement 2 fundamental methods.

class Dummy:
    def __str__(self) -> str:
        return 'Test'

    def __call__(self, scheme, *args, **kwargs):
       """
        Returned meta should be valid scheme
        Process your data and populate scheme struct
        src/core/scheme/definition.py
        
        :param scheme: MovieScheme object
        :returns: Scheme valid object list ex: {movie1, movie2}
        :rtype Generator[MovieScheme]
        """
        yield data
~~~~

Please see [example](https://github.com/ZorrillosDev/watchit-gateway/blob/master/resolvers/dummy/dummy.py)

### Scheme

The elaboration of the schema is quite simple, it consists in populate an array with dictionaries containing the
schematized metadata. Please
check [scheme definition](https://github.com/ZorrillosDev/watchit-gateway/blob/master/src/core/scheme/definition.py).

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
    type = fields.Str() # torrent | hls

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

## Usage

The process of evaluating the resolvers will determine the type of action to be executed in the VideoSchema |
ImageSchema:

When establishing a `cid`, the gateway just associate that hash to the metadata. If a URL is found, the gateway must
execute the download of the file in a directory associated with each movie and ingest it in IPFS to obtain its
corresponding `cid` and later associate it to the movie in the metadata:

**CID:**

If your content already exists in IPFS you just have to define it as follows.

 ```
"small_image": {"cid": "QmYNQJoKGNHTpPxCBPh9KkDpaExgd2duMa3aF6ytMpHdao"}, # Absolute cid
"medium_image": {"cid": "QmYNQJoKGNHTpPTYFSh9KkDpaExgd2iuMa3aF6ytMpPda2", "index": "myimage.jpg"},
"large_image": {"cid": "QmYNQJoKGNHTpPxCBPh9KkDpaExgd2duMa3aF6ytMpHdao"}, # Absolute cid
"date_uploaded_unix": 1446321498,
"resource": [
    {
        "cid": "QmYNQJoKGNHTpPxCBPh9KkDpaExgd2duMa3aF6ytMpHdao", # Example cid
        "index": "index.m3u8", # QmYNQJoKGNHTpPxCBPh9KkDpaExgd2duMa3aF6ytMpHdao/index.m3u8
        "quality": "720p",
        "type": "hls"
    }
]

```

**Note:** If you do not define an `index` in `resource` collection the `cid` must be absolute. If `index` is not defined
in `images` then default key `index` will be set

**URL**

If your files are in local env please use uri `file://` scheme. To migrate centralized remote or local data to
decentralized network need to define your schema as follow:

```
"small_image": {"url":" https://images-na.ssl-images-amazon.com/images/I/71-i1berMyL._AC_SL1001_.jpg"},
"medium_image": {"url":" https://images-na.ssl-images-amazon.com/images/I/71-i1berMyL._AC_SL1001_.jpg"},
"large_image": {"url":" https://images-na.ssl-images-amazon.com/images/I/71-i1berMyL._AC_SL1001_.jpg"},
"date_uploaded_unix": 1446321498,
"resource": [
    {
        "url": "https://movies.ssl-images-amazon.com/images/I/movie.m3u8",
        "index": "index.m3u8", 
        "quality": "720p",
        "type": "hls"
    }
]
```

**Note:** It will result in a directory structure after having downloaded the assets and ingested them into IPFS. As you
can see the `index` is used to define the name of the resulting path in the IPFS directory.

```
/{cid}
/{cid}/small_image.jpg
/{cid}/medium_image.jpg
/{cid}/large_image.jpg
/{cid}/index.m3u8

```

**Notes**

* 'url' and 'cid' are mutually exclusive
* If 'imdb_code' cannot be found for your movies please add your custom imdb_code ex: tt{movie_id}

**Caching**

After obtaining and schematizing the metadata these clean and pre-processed meta will be stored in a "temporary
collection cache" and in a "temporary collection cursor". The "temporary collection" keeps all the meta while
"the cursor collection" keeps the already processed meta to avoid unnecessary re-processing.

All this meta later will then be obtained and ingested in [OrbitDB](https://orbitdb.org/).

Please check some environment variables that are used to control this behavior:

```
# Flush tmp cache cursor
FLUSH_CACHE_IPFS=False
# Force get movies from source
REFRESH_MOVIES=False
# Force refresh IPFS ingestion
REFRESH_IPFS=True
# Create a new tmp collection version in each migration
REGEN_MOVIES=False
# Create a new source directory in each migration
REGEN_ORBITDB=False
```

## Run

1) Copy your custom module resolver to `resolvers` directory.
2) Start container `docker-compose up` to run migrator.
3) After finishing the migration process you can get the orbit addresses.
4) Copy the orbit address and use it when starting the [dapp](https://github.com/ZorrillosDev/watchit-desktop).





