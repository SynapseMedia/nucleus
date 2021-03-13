
## Usage

## Quick Summary
The process of evaluating the resolvers will determine the type of action to be executed in the schema definition:

When establishing a `route` that match a `cid` the gateway just associate that hash to the metadata. If an `route` match an `url` 
the gateway must execute the download of the `file` in a directory associated with each movie and ingest it in IPFS to obtain its
corresponding `cid` and later associate it to the movie in the metadata:

**CID:**

If your content already exists in IPFS you just have to define your scheme in resolver as follows.

 ```

"resource": {
    "images": {
        "small": {"route": "QmYNQJoKGNHTpPxCBPh9KkDpaExgd2duMa3aF6ytMpHdao"}, # Absolute cid
        "medium": {"route": "QmYNQJoKGNHTpPTYFSh9KkDpaExgd2iuMa3aF6ytMpPda2", "index": "myimage.jpg"},
        "large": {"route": "QmYNQJoKGNHTpPxCBPh9KkDpaExgd2duMa3aF6ytMpHdao"}, # Absolute cid
    }
    "videos: [
        {
            "route": "QmYNQJoKGNHTpPxCBPh9KkDpaExgd2duMa3aF6ytMpHdao", # Example cid
            "index": "index.m3u8", # QmYNQJoKGNHTpPxCBPh9KkDpaExgd2duMa3aF6ytMpHdao/index.torrent
            "quality": "720p",
            "type": "torrent"
        }
    ]
}

```

**Note:** If you do not define an `index` in `resource` collection the `route` `cid` must be absolute. 
If `index` is not defined in `images` collection then default key `index` will be set.

**URL**

If your files are in local env please use uri `file://` scheme. To migrate centralized remote or local data to
decentralized network need to define your schema in resolver as follows:

```

"resource": {
    "images": {
        "small": {"route":" https://images-na.ssl-images-amazon.com/images/I/71-i1berMyL._AC_SL1001_.jpg"},
        "medium": {"route":" https://images-na.ssl-images-amazon.com/images/I/71-i1berMyL._AC_SL1001_.jpg"},
        "large": {"route":" https://images-na.ssl-images-amazon.com/images/I/71-i1berMyL._AC_SL1001_.jpg"},
    },
    "videos": [
        {
            "route": "https://movies.ssl-images-amazon.com/I/720.m3u8",
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
/{cid}/{quality}/index.torrent

```

**Notes**

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
