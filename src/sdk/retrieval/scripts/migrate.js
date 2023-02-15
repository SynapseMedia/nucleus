"use strict"

// Please check orbitdb reference: 
// https://github.com/orbitdb/orbit-db/blob/main/API.md#orbitdbcreatename-type-options

const argv = require('minimist')(process.argv.slice(2));
const logs = console

const fs = require('fs')
const IpfsApi = require('ipfs-http-client');
const OrbitDB = require('orbit-db');
const { consume } = require('streaming-iterables')

const ORBIT_DB_NAME = argv.name || 'wt.movies.db' // The orbit db collection name
const MAX_CHUNKS = argv.size || 1000 // Max number of slices to group for CID
const IPFS_NODE = argv.node || '127.0.0.1' // Our local IPFS node

const TEST_MODE = argv.test || false
const OVERWRITE = argv.r || true // Overwrite existing database.
const KEY = argv.key || 'watchit' // Local key 
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
    const orbitdb = await OrbitDB.createInstance(IPFSLocalNode, {
        directory: `./${KEY}`
    });

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

// List of default keys
// ; = ensures the preceding statement was closed
; (async () => {
    if (TEST_MODE) {
        /**
         * IMPORTANT!
         * We use this flag for test only purpose.
         */
        logs.info("Waiting for data")
        let data = fs.readFileSync(0, 'utf-8');
        logs.info(data)
        process.exit(0)
        return
    }

    // Initialize orbit db log
    logs.info(`Starting ${KEY} db `);
    const db = await initializeOrbit(ORBIT_DB_NAME, { overwrite: OVERWRITE })
    const dbAddress = db.address.toString()
    const dbAddressHash = dbAddress.split('/')[2]

    // Check if existing keys else create it
    if (!(await hasIPFSKey(KEY))) {
        await IPFSLocalNode.key.gen(KEY)
        logs.warn(`"${KEY}" key created`)
    }

    // let others know that we exist
    // const ipns = await announceDB(dbAddressHash)

    // Start movies migration to orbit from mongo
    let index = 0; // Keep cursor for movies unique id

    try {

        const size = rawData.length
        const data = generateChunks(rawData, MAX_CHUNKS);

        logs.warn(`Migrating ${size} movies..`)

        for (const chunk of data) {
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
