const IPFS = require('ipfs')
const OrbitDB = require('orbit-db')
const p2p = require('./p2p')

//gAl3X#0205??M
args = process.argv.slice(2);
const HASH = args[0];
const DB = args[1];
const FOLDER_NAME = args[2] !== 'false' ? args[2] : false;
const IPFS_NODE = args[3] === 'false' ? false : args[3] || 'QmUFMXkMrv3TJbgCrAQ8raTWcJo6fQgJE3HQgGxw3nmFYB';
const IPFS_IP = args[4] || '167.71.11.115';

const CONF = {
	libp2p: p2p,
	repo: FOLDER_NAME && `source/ipfs_${FOLDER_NAME}` || 'source/ipfs',
};

(async () => {
    try {
        // Create IPFS instance
        console.log(`Running ipfs node`);
        const ipfs = await IPFS.create(CONF);
        const id = await ipfs.id()

        console.log('Setting up node..', id.id);
        IPFS_NODE && await ipfs.swarm.connect(`/ip4/${IPFS_IP}/tcp/4002/ws/p2p/${IPFS_NODE}`);

        // Create OrbitDB instance
        console.log('Loading db..')
        const orbitdb = await OrbitDB.createInstance(ipfs, {
            ...FOLDER_NAME && {
                directory: `source/orbit_${FOLDER_NAME}`
            }
        });

        const dbAddress = `/orbitdb/${HASH}/${DB}`;
        const db = await orbitdb.open(dbAddress, {
            replicate: true, sync: true
        });

        // console.log('Starting db..')
        db.events.on('peer', (p) => console.log('Peer:', p))
        // // db.events.on('replicate', (address) => console.log('Replicate', address))
        db.events.on('replicate.progress', (address, hash, entry, progress, total) => {
            // console.log(entry.payload.value['torrents']);
            console.log(total);
            console.log('Memory:', (process.memoryUsage().heapUsed / 1024 / 1024).toFixed(2), 'Mb');
            console.log(((progress / total) * 100).toFixed(1), '%')
        })

        db.events.on('load.progress', (address, hash, entry, progress, total) => {
            console.log('Loading cache..')
            console.log(((progress / total) * 100).toFixed(1), '%')
        })

        db.events.on('replicated', (address) => {
            console.log('Replicated', address)
            // console.log(db.get(''))
        })

        db.load()

    } catch (err) {
        console.log(err);
    }

})()
