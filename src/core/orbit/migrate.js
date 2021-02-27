const argv = require('minimist')(process.argv.slice(2));

const MAX_CHUNKS = 1000
const DB_MOVIES = 'wt.movies.db'
const SOURCE_DB = argv.source || 'ipfs';
const IPFS_NODE = argv.node || 'ipfs'
const KEY = argv.key || 'watchit' // Local key used to IPNS publish
const MONGO_DB = argv.hdb || 'mongodb' // Temporary helper db
const PDM = argv.p // Activate PDM filter
const RECREATE = argv.r || true // Recreate database
const REGEN = argv.g || false

const ligLogger = require('@liquicode/lib-logger');
const logs = ligLogger.NewConsoleLogger()
const IpfsApi = require('ipfs-http-client');
const OrbitDB = require('orbit-db');
const {consume} = require('streaming-iterables')
const MongoClient = require('mongodb').MongoClient;
const ipfs = IpfsApi({host: IPFS_NODE, port: '5001', protocol: 'http'});
const msgpack = require("msgpack-lite");
const {v4: uuidv4} = require('uuid');


(async () => {
    try {
        logs.info(`Connecting ipfs node`);
        const chunkGen = (_movies, l) => {
            return new Array(Math.ceil(_movies.length / l)).fill(0)
                .map((_, n) => _movies.slice(n * l, n * l + l));
        }

        // Create OrbitDB instance
        const DB_NAME = SOURCE_DB;
        const DB_OPTIONS = {overwrite: RECREATE, localOnly: false, replicate: true}
        const orbitdb = await OrbitDB.createInstance(ipfs, {
            directory: REGEN ? `./orbit${uuidv4()}` : './orbit'
        });

        // DB
        const db = await orbitdb.log(DB_MOVIES, DB_OPTIONS);
        db.events.on('peer', (p) => logs.warn('Peer Db:', p));

        // END DB
        const definedType = PDM ? 'PDM' : 'W';
        logs.info(`Starting ${definedType} db `);
        const dbAddress = db.address.toString()
        const dbAddressHash = dbAddress.split('/')[2]

        //Add provider to allow nodes connect to it
        logs.info(`Providing addressfor ${definedType}`);
        await consume(ipfs.dht.provide(dbAddressHash))
        logs.info(`Publishing address for ${definedType}`)
        const ipns = await ipfs.name.publish(dbAddressHash, {key: KEY})
        logs.warn(`Publish done for for ${definedType}`, ipns.name)


        // Start movies migration to orbit from mongo
        logs.trace('Saving data..');
        let index = 0; // Keep cursor for movies id
        const url = `mongodb://${MONGO_DB}`;
        const client = new MongoClient(url, {useUnifiedTopology: true});
        await client.connect(async () => {
            // Generate cursor for all movies
            const adminDb = client.db(DB_NAME)
            const cursor = adminDb.collection('movies').find(
                {...PDM && {pdm: true}}
            ).limit(0).sort({year: 1})
            const size = await cursor.count();
            const data = chunkGen(await cursor.toArray(), MAX_CHUNKS);
            logs.info('Total movies:', size)

            for (const chunk of data) {
                // let before = +new Date();
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

                await db.add(
                    cid.cid.toString()
                );

                // console.log('Processed: ', `${index}/${size}`);
                // console.log('Last id:', index);
                // console.log('Memory:', (process.memoryUsage().heapUsed / 1024 / 1024).toFixed(2), 'Mb');
                // console.log('Time Elapsed:', (+new Date() - before) / 1000 | 0);
                // console.log('Created: ', cid.cid.toString());
            }

            await client.close();
            logs.info('Processed: ', `${index}/${size}`);
            logs.warn('Address:', `${dbAddressHash}`)
            logs.trace('Closed db..');
        });

    } catch (err) {
        logs.error(err);
    }

})()
