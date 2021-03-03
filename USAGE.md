
## Usage

The process of evaluating the resolvers will determine the type of action to be executed in the VideoSchema |
ImageSchema:

When establishing a `cid`, the gateway just associate that hash to the metadata. If an `url` is found, the gateway must
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
in `images` collection then default key `index` will be set.

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
        "url": "https://movies.ssl-images-amazon.com/I/movie.mp4",
        "index": "index.mp4", 
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
/{cid}/index.mp4

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