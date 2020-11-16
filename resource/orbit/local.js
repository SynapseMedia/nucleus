const IpfsApi = require('ipfs-http-client');
const OrbitDB = require('orbit-db')

args = process.argv.slice(2);
const HASH_CLIENT = args[0];
const HASH_MOVIES = args[1];


(async () => {
    try {
        console.log(`Running ipfs node`);
        // Create OrbitDB instance
        console.log('Loading db..')
        const ipfs = IpfsApi();
        const orbitdb = await OrbitDB.createInstance(ipfs);

        console.log('Starting db movies..')
        const dbAddress = `/orbitdb/${HASH_MOVIES}/wt.movies.db`;
        const db = await orbitdb.open(dbAddress, {
            sync: true, replicate: true
        });

        db.events.on('peer', (p) => console.log('Peer Client:', p));
        db.events.on('replicate.progress', async (address, hash, entry, progress, total) => {
            console.log(total);
            console.log(((progress / total) * 100).toFixed(1), '%')
        })

        db.events.on('load.progress', (address, hash, entry, progress, total) => {
            console.log('Loading cache..')
            console.log(((progress / total) * 100).toFixed(1), '%')
        })

        // Open replicate clients
        console.log('Starting db c..')
        const dbClientAddress = `/orbitdb/${HASH_CLIENT}/wt.c.db`;
        const dbClient = await orbitdb.open(dbClientAddress, {
            sync: true, replicate: true
        });

        dbClient.events.on('peer', (p) => console.log('Peer Db:', p));
        dbClient.events.on('replicate.progress', (address, hash, entry, progress, total) => {
            console.log(((progress / total) * 100).toFixed(1), '%')
        })

        dbClient.events.on('load.progress', (address, hash, entry, progress, total) => {
            console.log('Loading cache c..')
            console.log(((progress / total) * 100).toFixed(1), '%')
        })

        // db.load()
        // dbClient.load()

    } catch (err) {
        console.log(err);
    }

})()
