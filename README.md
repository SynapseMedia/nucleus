# Gateway Watchit Seeder

[![Gitter](https://badges.gitter.im/watchit-app/community.svg)](https://gitter.im/watchit-app/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

## Getting started

* If you don’t have Go, [install it](https://golang.org/doc/install).
* If you don’t have IPFS , [install it](https://github.com/ipfs/go-ipfs#install).
* [Spawn go-ipfs node with docker](https://mrh.io/ipfs_docker/).
* [How to spawn an IPFS node in Node.js](https://mrh.io/2018-01-24-pushing-limits-ipfs-orbitdb/).
* For private networks [How to spawn an IPFS private node and generate swarm key](https://mrh.io/ipfs-private-networks/)
  .

## Quick summary

The watchit gateway is an interface or micro framework for the migration of content to IPFS and the distribution of
metadata through OrbitDB.

Watchit gateway adds migrated data to the metastore (orbitdb) which is distributed in a predefined scheme definition to
ensure the integrity of the data that is later consumed by
the [application](https://github.com/ZorrillosDev/watchit-desktop). Watchit gateway provides simple tools for the
generation and acquisition of content.

## Tools

### Resolvers

"A _resolver_ is a set of instructions, expressed as a Python class. A _gateway_ will execute a resolver to fetch
content from various sources." - @aphelionz

Resolvers implement the logic necessary for the acquisition, preprocessing, cleaning and schematization of data from any
available resource. Based on the following class abstraction we can see the methods required for the development of a
resolver:

~~~~
Define your resolvers modules below.
Ex: Each resolver must implement 2 fundamental methods.

class Dummy:
    def __str__(self) -> str:
        return 'Test'

    def __call__(self, scheme, *args, **kwargs) -> iter:
       """
        Returned meta should be valid scheme
        Process your data and populate scheme struct
        src/core/scheme/definition.py
        :param scheme: Scheme object
        :yield object: Scheme valid
        """
        yield data
~~~~

Please see [example](https://github.com/ZorrillosDev/watchit-gateway/blob/master/resolvers/dummy/dummy.py)

### Scheme

The elaboration of the schema is quite simple, it consists in populate an array with dictionaries containing the
schematized metadata:

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
  # Public domain movie?
  pdm = fields.Bool(default=False)
  trailer_code = fields.Str(missing=None)  # Youtube trailer code
  # https://meta.wikimedia.org/wiki/Template:List_of_language_names_ordered_by_code
  language = fields.Str(validate=validate.Length(min=2, max=10))
  # https://en.wikipedia.org/wiki/Motion_Picture_Association_film_rating_system
  mpa_rating = fields.Str(default='PG')
  # This uri links should be declared to IPFS ingestion
  small_cover_image = fields.Nested(ImageScheme())
  medium_cover_image = fields.Nested(ImageScheme())
  large_cover_image = fields.Nested(ImageScheme())
  resource = fields.List(fields.Nested(ResourceScheme()))
  date_uploaded_unix = fields.Int()
```

#### ResourceScheme

    url = fields.Url(relative=True)  # Remote file
    cid = fields.Str()  # CID hash 
    index = fields.Str()  # File index in CID directory
    quality = fields.Str(required=True)  # 720p | 1080p | 2048p | 3D
    type = fields.Str() # torrent | hls

#### ImageScheme

    url = fields.Url(relative=True)  # Remote file
    cid = fields.Str()  # CID hash

## Underneath

The process of evaluating the resolvers will determine the type of action to be executed in the ResourceSchema |
ImageSchema:

When establishing a `cid`, the gateway just associate that hash to the metadata. If a URL is found, the gateway must
execute the download of the file in a directory associated with each movie and ingest it in IPFS to obtain its
corresponding hash and later associate it to the movie in the metadata:

**CID:**

If your content already exists in IPFS you just have to define it as follows.

If you do not define an `index` in `resource` the `cid` must be absolute. If `index` not defined in `images` default
key `index` will be set

 ```
"small_cover_image": {"cid": "QmYNQJoKGNHTpPxCBPh9KkDpaExgd2duMa3aF6ytMpHdao"}, # Absolute cid
"medium_cover_image": {"cid": "QmYNQJoKGNHTpPTYFSh9KkDpaExgd2iuMa3aF6ytMpPda2", "index": "myimage.jpg"},
"large_cover_image": {"cid": "QmYNQJoKGNHTpPxCBPh9KkDpaExgd2duMa3aF6ytMpHdao"}, # Absolute cid
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

**URL**

```
"small_cover_image": {"url":" https://images-na.ssl-images-amazon.com/images/I/71-i1berMyL._AC_SL1001_.jpg"},
"medium_cover_image": {"url":" https://images-na.ssl-images-amazon.com/images/I/71-i1berMyL._AC_SL1001_.jpg"},
"large_cover_image": {"url":" https://images-na.ssl-images-amazon.com/images/I/71-i1berMyL._AC_SL1001_.jpg"},
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

It will result in a directory structure after having downloaded the assets and ingested them into IPFS. As you can see
the `index` is used to define the name of the resulting path in the IPFS directory

```
/{cid}
/{cid}/small_cover_image.jpg
/{cid}/medium_cover_image.jpg
/{cid}/large_cover_image.jpg
/{cid}/index.m3u8

```

**Notes**

* If 'imdb_code' cannot be found add your custom imdb_code ex: tt{movie_id}
* 'url' and 'hash' are mutually exclusive

Please
check [scheme definition](https://github.com/ZorrillosDev/watchit-gateway/blob/master/src/core/scheme/definition.py)

## Run

*Start docker containers and starts movies migration.*
> Run seeder IPFS public node.

`docker-compose up`
