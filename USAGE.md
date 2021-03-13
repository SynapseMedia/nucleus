
# Usage

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

**URL:**

If your files are in local env please use uri `file://` scheme. To migrate centralized remote or local data to
decentralized network need to define your schema in resolver as follows:

```

"resource": {
    "images": {
        "small": {"route":"https://movies.example.com/images/small.jpg"},
        "medium": {"route":"https://movies.example.com/images/medium.jpg"},
        "large": {"route":"https://movies.example.com/images/large.jpg"},
    },
    "videos": [
        {
            "route": "https://movies.example.com/I/720.m3u8",
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
/{cid}/small.jpg
/{cid}/medium.jpg
/{cid}/large.jpg
/{cid}/{quality}/index.m3u8

```

**IMPORTANT!** If 'imdb_code' cannot be found for your movies please add your custom imdb_code ex: tt{movie_id}

## Caching

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

1) Clone the repo using git command `git clone https://github.com/ZorrillosDev/watchit-gateway`
2) Please [install docker](https://docs.docker.com/get-started/) and [docker-compose](https://docs.docker.com/compose/install/)
3) Inside the `repo` root search for `resolvers` directory
   ```
   /watchit-gateway/
   /watchit-gateway/resolvers/
   ```
4) Copy your custom resolver to `resolvers` directory.
    ```
   /watchit-gateway/
   /watchit-gateway/resolvers/
   /watchit-gateway/resolvers/{resolver_here}/
   ```
   Please check our [example](https://github.com/ZorrillosDev/watchit-gateway/tree/v0.1.0/resolvers)
5) Start container using `docker-compose up` to start migration.
3) Please wait to finishing the migration process then you will can get the orbit addresses. eg:
   
   ```
   CID: zdpuB24EVZjCaeZcqCNP9EPXtNguqj4qV6W13QWDPPUe6RtNF
   IPNS: QmNr4dkAbUtBXCzwYXEJX7XW8bhNwk1vwoiUYnMD8VNyS6 # Use IPNS to keep using same hash for your channel
   ```
4) Copy the orbit address (CID or IPNS) and use it as **Public Key** when starting the [dapp](https://github.com/ZorrillosDev/watchit-desktop).


