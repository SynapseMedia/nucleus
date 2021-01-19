args = process.argv.slice(2);

const MAX_CHUNKS = 1000
const DB_MOVIES = 'wt.movies.db'
const MONGO_DB = args[0] || 'mongodb'
const SOURCE_DB = args[1] || 'ipfs';
const IPFS_NODE = args[2] || 'ipfs'
const RECREATE = args[3] !== 'false';

const IpfsApi = require('ipfs-http-client');
const OrbitDB = require('orbit-db');
const MongoClient = require('mongodb').MongoClient;
const ipfs = IpfsApi({host: IPFS_NODE, port: '5001', protocol: 'http'});
const msgpack = require("msgpack-lite");

(async () => {
    try {
        console.log(`Starting ipfs node`);
        // const ipfs = await IPFS.create(CONF);
        console.log('Setting up node..');
        const chunkGen = (_movies, l) => {
            return new Array(Math.ceil(_movies.length / l)).fill(0)
                .map((_, n) => _movies.slice(n * l, n * l + l));
        }

        // Create OrbitDB instance
        const DB_NAME = SOURCE_DB;
        const orbitdb = await OrbitDB.createInstance(ipfs);

        // DB
        const db = await orbitdb.log(DB_MOVIES, {
            overwrite: RECREATE,
            localOnly: false,
            replicate: true
        });
        // END DB

        console.log('Starting db..');
        console.log(db.address.toString());
        db.events.on('peer', (p) => console.log('Peer Db:', p));

        // MOVIES
        let index = 0;
        const url = `mongodb://${MONGO_DB}`;
        const client = new MongoClient(url, {useUnifiedTopology: true});
        await client.connect(async () => {
            // Generate cursor for all movies
            const adminDb = client.db(DB_NAME)
            const cursor = adminDb.collection('movies').find({}).limit(0).sort({year: 1})
            const size = await cursor.count();
            const data = chunkGen(await cursor.toArray(), MAX_CHUNKS);
            console.log('Total movies:', size)

            for (const chunk of data) {
                console.log('Starting');
                console.log('Chunk size:', chunk.length)

                let before = +new Date();
                let ch = chunk.map((v) => {
                    index++;
                    v['_id'] = `wt_loc_${index}`;
                    v['total'] = size;

                    if ('torrents' in v) {
                        for (const value of v.torrents) {
                            delete value['url'];
                        }
                    }

                    delete v['url']
                    delete v['state']
                    return v
                });

                //Add movie
                console.log('Adding to network');
                let cid = await ipfs.add(
                    msgpack.encode(ch),
                    {pin: true}
                );

                await db.add(cid.cid.toString());
                console.log('Saving data..');
                console.log('Processed: ', `${index}/${size}`);
                console.log('Last id:', index);
                console.log('Memory:', (process.memoryUsage().heapUsed / 1024 / 1024).toFixed(2), 'Mb');
                console.log('Time Elapsed:', (+new Date() - before) / 1000 | 0);
                console.log('Created: ', cid.cid.toString());
            }

            await client.close();
            console.log('Closed db..');
        });

    } catch (err) {
        console.log(err);
    }

})()
