process.env.FORCE_COLOR = 1
const argv = require('minimist')(process.argv.slice(2));
const IPFS_NODE = argv.node || 'watchit-ipfs'
const MONITOR_INTERVAL = argv.timer || process.env.MONITOR_INTERVAL
const MONITOR_CID = argv.monitor || process.env.MONITOR_CID
const last = require('it-last')
const IpfsApi = require('ipfs-http-client');
const {CID} = require('ipfs-http-client')
const {base58btc} = require('multiformats/bases/base58')
const ipfs = IpfsApi.create({host: IPFS_NODE, port: '5001', protocol: 'http'});
const OrbitDB = require('orbit-db');
const logs = require('./logger')

// List of default keys
// ; = ensures the preceding statement was closed

const pin = async (cid) => {
    logs.info(`Fetching block ${cid}`)
    await ipfs.pin.add(cid)
    logs.info(`Pinning hash ${cid}`)
}

const iterateOverReplica = async (db) => {
    db.iterator({limit: -1}).collect().map(async (e) => {
        await pin(e.payload.value)
    })
}

async function runMapper() {
    // Get monitor CID from IPNS
    logs.info(`Resolving CID mapper ${MONITOR_CID}`)
    const resolvedCid = await last(ipfs.name.resolve(MONITOR_CID))
    const cid = resolvedCid.split('/').pop()
    const addressIPNSList = await last(ipfs.cat(cid))
    const addressListString = addressIPNSList.toString()

    for (const address of addressListString.split('\n')) {
        if (!address) continue

        logs.info(`Resolving address from IPNS: ${address}`)
        const cid = await last(ipfs.name.resolve(address))
        const cleanedCID = cid.split('/').pop()
        const newCID = CID.parse(cleanedCID)
        const _address = newCID.toString(base58btc)

        logs.info(`Resolved orbit address: ${_address}`)
        const orbitdb = await OrbitDB.createInstance(ipfs);

        logs.info(`Opening database from ${_address}`)
        const db = await orbitdb.log(`/orbitdb/${_address}/wt.movies.db`, {
            sync: true,
            overwrite: true,
            localOnly: false
        })

        logs.info('Listening for updates to the database...')
        db.events.on('ready', () => iterateOverReplica(db))
        await db.load()
        return [db, orbitdb];
    }
}

;(async function start() {
    logs.info('Running Pinning Service')
    const [db, orbitdb] = await runMapper() // Initial mapper start
    logs.info('Setting interval')
    setInterval(async () => {
        // Force restart docker
        await orbitdb.stop();
        await db.drop();
        await start()
    }, MONITOR_INTERVAL * 60 * 1000)
})()

