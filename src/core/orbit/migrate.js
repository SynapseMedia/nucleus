const argv = require('minimist')(process.argv.slice(2));

const MAX_CHUNKS = 1000
const ORBIT_DB_NAME = 'wt.movies.db'
const MIGRATE_FROM_DB = argv.source || 'ipfs';

const IPFS_NODE = argv.node || 'ipfs'
const MONGO_HOST = argv.hdb || 'mongodb' // Temporary helper db

const PDM = argv.p // Activate PDM filter
const RECREATE = argv.r || true // Recreate database
const KEY = argv.key || 'watchit' // Local key used to IPNS publish
const REGEN = argv.g || false


const IpfsApi = require('ipfs-http-client');
const OrbitDB = require('orbit-db');
const {consume} = require('streaming-iterables')
const MongoClient = require('mongodb').MongoClient;
const logs = require('pino')({prettyPrint: {colorize: true}})
const ipfs = IpfsApi({host: IPFS_NODE, port: '5001', protocol: 'http'});
const msgpack = require("msgpack-lite");
const {v4: uuidv4} = require('uuid');


(async () => {

    logs.info(`Connecting ipfs node`);
    const chunkGen = (_movies, l) => {
        return new Array(Math.ceil(_movies.length / l)).fill(0)
            .map((_, n) => _movies.slice(n * l, n * l + l));
    }

    // Create OrbitDB instance
    const DB_NAME = MIGRATE_FROM_DB;
    const DB_OPTIONS = {overwrite: RECREATE, localOnly: false, replicate: true}
    const orbitdb = await OrbitDB.createInstance(ipfs, {
        directory: REGEN ? `./orbit${uuidv4()}` : './orbit'
    });

    // DB
    const db = await orbitdb.log(ORBIT_DB_NAME, DB_OPTIONS);
    db.events.on('peer', (p) => logs.warn('Peer Db:', p));

    // END DB
    const definedType = PDM ? 'PDM' : 'All';
    logs.info(`Starting ${definedType} db `);
    const dbAddress = db.address.toString()
    const dbAddressHash = dbAddress.split('/')[2]

    //Add provider to allow nodes connect to it
    logs.info(`Providing address for ${definedType}`);
    await consume(ipfs.dht.provide(dbAddressHash))
    logs.info(`Publishing address for ${definedType}`)
    const ipns = await ipfs.name.publish(dbAddressHash, {key: KEY})
    logs.warn(`Publish done for for ${definedType}`, ipns.name)


    // Start movies migration to orbit from mongo
    let index = 0; // Keep cursor for movies id
    const url = `mongodb://${MONGO_HOST}`;
    const client = new MongoClient(url, {
        useUnifiedTopology: true,
        keepAlive: true
    });

    try {
        logs.warn('Connecting to helper db..');
        await client.connect(async (err) => {

            console.log(DB_NAME)
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

        })

        logs.info('Processed: ', `${index}/${size}`);
        logs.warn('Address:', `${dbAddressHash}`)

    } catch (err) {
        logs.error(err);
    } finally {
        await client.close();
        logs.warn('Closed db..');
    }

})()
