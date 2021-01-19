const IpfsApi = require('ipfs-http-client');
const OrbitDB = require('orbit-db')
const fs = require('fs')
const path = require('path')

args = process.argv.slice(2);
const address = args[0] || fs.readFileSync(
    path.join(process.cwd(), 'hash'),
    {encoding: 'utf8', flag: 'r'}
);

(async () => {
    try {
        console.log(`Running ipfs node`);
        // Create OrbitDB instance
        console.log('Loading db..')
        const ipfs = IpfsApi();
        const orbitdb = await OrbitDB.createInstance(ipfs);

        for await (const cid of ipfs.dht.findProvs(address)) {
            console.info('Connecting to:', cid.id)
            const mAddr = cid.addrs.map((m) => `${m.toString()}/p2p/${cid.id}`)

            for (const m of mAddr) {
                try {
                    await ipfs.swarm.connect(m, {timeout: 1000})
                    console.log(`Connected to`, m);
                } catch (e) {
                    console.log(`Cannot connect to`, m);
                }
            }
        }

        console.log('Starting db movies..')
        const dbAddress = `/orbitdb/${address}/wt.movies.db`;
        const db = await orbitdb.open(dbAddress, {sync: true, replicate: true});

        // Events handlers
        db.events.on('peer', (p) => console.log('Peer Client:', p));
        db.events.on('replicate.progress', async (address, hash, entry, progress, total) => {
            console.log(total);
            console.log(((progress / total) * 100).toFixed(1), '%')
        })

        db.events.on('load.progress', (address, hash, entry, progress, total) => {
            console.log('Loading cache..')
            console.log(((progress / total) * 100).toFixed(1), '%')
        })

    } catch (err) {
        console.log(err);
    }

})()
