process.env.FORCE_COLOR = 1
const argv = require('minimist')(process.argv.slice(2));

const IPFS_NODE = 'ipfs'
const MONITOR_INTERVAL = process.env.MONITOR_INTERVAL
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

// Get monitor CID from IPNS
let inProgress = new Set();
setInterval(async () => {
    logs.info(`Resolving CID mapper ${MONITOR_CID}`)
    const resolvedCid = await last(ipfs.name.resolve(MONITOR_CID))
    const cid = resolvedCid.split('/').pop()
    const addressIPNSList = await last(ipfs.cat(cid))
    const addressListString = addressIPNSList.toString()

    for (const address of addressListString.split('\n')) {
        if (!address) continue
        // Avoid re-open address
        if (inProgress.has(address)) continue
        inProgress.set(address)

        logs.info(`Resolving address from IPNS: ${address}`)
        const cid = await last(ipfs.name.resolve(address))
        const cleanedCID = cid.split('/').pop()
        const newCID = CID.parse(cleanedCID)
        const addr = newCID.toString(base58btc)
        logs.info(`Resolved orbit addressS: ${addr}`)

        const orbitdb = await OrbitDB.createInstance(ipfs);
        logs.info(`Opening database from ${addr}`)
        const db = await orbitdb.open(`/orbitdb/${addr}/wt.movies.db`, {replicate: true})

        logs.info('Listening for updates to the database...')
        db.events.on('ready', () => logs.info("Db ready"))
        db.events.on('replicated', (address, t) => logs.info(`Replicated ${t}`))
        db.events.on('replicate.progress', (address, hash, entry, progress, have) => {
            logs.info(entry)
        })
    }
}, MONITOR_INTERVAL * 60 * 1000)
