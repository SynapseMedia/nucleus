"use strict"

// Please check orbitdb reference: 
// https://github.com/orbitdb/orbit-db/blob/main/API.md#orbitdbcreatename-type-options

const argv = require('minimist')(process.argv.slice(2));
const logs = require('./logger');

const IpfsApi = require('ipfs-http-client');
const OrbitDB = require('orbit-db');
const Sqlite3 = require("sqlite3").verbose()
const { consume } = require('streaming-iterables')

const ORBIT_DB_NAME = argv.name || 'wt.movies.db' // The orbit db collection name
const MAX_CHUNKS = argv.size || 1000 // Max number of slices to group for CID
const SOURCE_DB = argv.db || 'watchit.db'; // From where we get the raw data
const IPFS_NODE = argv.node || 'watchit-ipfs' // Our local IPFS node

const OVERWRITE = argv.r || true // Overwrite existing database.
const COLLECTOR = argv.s || 'FULL' // Collector name to migrate source. This could be useful if we need to create different 
const KEY = argv.key || 'watchit' // Local key used to IPNS publish

const IPFSLocalNode = IpfsApi.create({ host: IPFS_NODE, port: '5001', protocol: 'http' });
/**
 * Split array in fixed size chunks
 *
 * @param {*} array
 * @param {*} len
 * @return {*} 
 */
function generateChunks(array, len) {
    // Split array in chunks
    return new Array(Math.ceil(array.length / len)).fill(0)
        .map((_, n) => array.slice(n * len, n * len + len));
};

/**
 * Check if a key is registered in local node
 *
 * @param {*} node
 * @param {*} key
 * @return {*} 
 */
async function hasIPFSKey(key) {
    // Check if current used key exists
    const currentList = await IPFSLocalNode.key.list()
    return currentList.some((k) => Object.is(k.name, key))
};

/**
 * Initialize and setup orbit db database
 *
 * @param {*} dbName
 * @param {*} [options={}]
 * @return {*} 
 */
async function initializeOrbit({ options = {} }) {
    // Create OrbitDB instance
    const dbOptions = { ...{ overwrite: OVERWRITE, localOnly: false, replicate: true }, ...options }
    const orbitdb = await OrbitDB.createInstance(IPFSLocalNode);

    // Initialize orbit db log
    const db = await orbitdb.log(ORBIT_DB_NAME, dbOptions);
    db.events.on('peer', (p) => logs.warn(`Peer Db: ${p}`));
    return db
}

/**
 * Keep locked database address over IPNS and announce address to DHT.
 * The idea here is avoid change the address every time that we create a new orbit database.
 * The DHT approach is try to reach faster and sync with genesis node querying the DHT table in the remote side.
 * 
 * @param {*} address 
 * @returns IPNS address for orbit address
 */
async function announceDB(address) {
    logs.info('Announce address over DHT')
    // Add provider to allow nodes connect to it
    await consume(IPFSLocalNode.dht.provide(address))
    return await IPFSLocalNode.name.publish(address, { key: KEY })
}


/**
 * Collect and convert data from serialized sqlite3 entries
 *
 * @param {*} db
 * @returns Out of the box data
 */
async function collectDataFromCache(db) {
    const db = new Sqlite3.Database(db)
    const query = "SELECT * FROM movies"
    const data = db.map(query, (err, row) => {

    })
}

// List of default keys
// ; = ensures the preceding statement was closed
; (async () => {

    // Initialize orbit db log
    logs.info(`Starting ${COLLECTOR} db `);
    const db = initializeOrbit(ORBIT_DB_NAME, { overwrite: OVERWRITE })
    const dbAddress = db.address.toString()
    const dbAddressHash = dbAddress.split('/')[2]

    // Check if existing keys else create it
    if (!(await hasIPFSKey(IPFSLocalNode, KEY))) {
        await IPFSLocalNode.key.gen(KEY)
        logs.warn(`"${KEY}" key created`)
    }

    // let others know that we exist
    const ipns = announceDB(dbAddress)

    // Start movies migration to orbit from mongo
    let index = 0; // Keep cursor for movies unique id

    try {
        logs.warn('Connecting to cache..');
        const rawData = collectDataFromCache(SOURCE_DB)
        const size = rawData.length
        const data = generateChunks(rawData, MAX_CHUNKS);
    
        logs.warn(`Migrating ${size} movies..`)

        for (const chunk of rawData) {
            // let before = +new Date();
            let ch = chunk.map((v) => {
                index++;
                v['_id'] = `wt_loc_${index}`;
                v['total'] = size;
                return v
            });
            //Add movie
            const { cid } = await IPFSLocalNode.add(
                Buffer.from(JSON.stringify(ch)),
                { pin: true }
            );

            await db.add(cid.toString());
            logs.info(`Chunk CID: ${cid.toString()}`)
            logs.info(`Processed: ${index}/${size}`);
        }

        logs.success(`CID for ${definedType}: ${dbAddressHash}`)
        logs.success(`IPNS for ${definedType}: ${ipns.name}`)
        await client.close();
        logs.warn('Closed db..\n');


    } catch (err) {
        logs.error(err);
    }

}
)()
