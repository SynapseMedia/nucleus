process.env.FORCE_COLOR = 1
const argv = require('minimist')(process.argv.slice(2));
const proc = require('process')
const IPFS_NODE = 'watchit-ipfs'
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
;(async () => {
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
        const db = await orbitdb.open(`/orbitdb/${_address}/wt.movies.db`, {sync: true})

        logs.info('Listening for updates to the database...')
        db.events.on('ready', () => logs.info("Db ready"))
        await db.load()
        console.log(await db.iterator({limit: -1}).collect());

    }

    setTimeout(() => {
        // Force restart docker
        logs.warn("Killing process")
        proc.exit(0)
    }, MONITOR_INTERVAL * 60 * 1000)

})()