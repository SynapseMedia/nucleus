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

###Resolvers

Resolvers implement the logic necessary for the acquisition, preprocessing, cleaning and schematization of data from any
available resource. Based on the following class abstraction we can see the methods required for the development of a
resolver:

~~~~
Define your resolvers modules below.
Ex: Each resolver must implement 2 fundamental methods.

class Dummy:
    def __str__(self) -> str:
        return 'Test'

    def __call__(self, *args, **kwargs) -> iter:
        """
        Process your data and populate scheme struct
        src/core/scheme/definition.py
        """
        yield data
~~~~

Please see [example](https://github.com/ZorrillosDev/watchit-gateway/blob/master/resolvers/dummy/dummy.py)

###Scheme

The elaboration of the schema is quite simple, it consists of a popular arrangement with dictionaries containing the
metadata example:

####MovieScheme
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
  pdm = fields.Bool(default=False)
  trailer_code = fields.Str(missing=None)  # Youtube trailer code
  # https://meta.wikimedia.org/wiki/Template:List_of_language_names_ordered_by_code
  language = fields.Str(validate=validate.Length(min=2, max=10))
  # https://en.wikipedia.org/wiki/Motion_Picture_Association_film_rating_system
  mpa_rating = fields.Str(default='PG')
  # This uri links should be declared to IPFS ingestion
  small_cover_image = fields.Url(required=True)
  medium_cover_image = fields.Url(required=True)
  large_cover_image = fields.Url(required=True)
  resource = fields.List(fields.Nested(ResourceScheme()))
  date_uploaded_unix = fields.Int()
```

####ResourceScheme
    url = fields.Url(required=False, relative=True)  # File link
    hash = fields.Str(required=False)  # CID hash
    index = fields.Str(required=True)  # File index in hash directory
    quality = fields.Str(required=True)  # Quality ex: 720p, 1080p..
    type = fields.Str(validate=validate.OneOf(ALLOWED_FORMATS))

**Notes**
  
    * ResourceScheme:
      * index its the file system file to be retrieved ex:
          https://gateway.ipfs.io/hash/index.movie


**Exceptions:**

    * MovieScheme: 
        * If 'imdb_code' cannot be found add your custom imdb_code ex: tt{movie_id}
    * ResourceScheme: 
        * If 'url' its declared gateway will try to migrate content to IPFS.
        * If 'hash' its declared 'url' will be omitted and 'hash' will be keeped.

## Run

*Start docker containers and starts movies migration.*
> Run seeder/bootstrap IPFS public node.

`docker-compose up`
