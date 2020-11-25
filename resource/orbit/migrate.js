args = process.argv.slice(2);

const MAX_CHUNKS = 1000
const SKIP_CLIENTS = false
const DB_MOVIES = 'wt.movies.db'
const MONGO_DB = args[0] || 'watchit_mongo'
const IPFS_NODE = args[2] || 'watchit_ipfs'
const SOURCE_DB = args[1] || 'witth20201124';
const RECREATE = args[3] !== 'false';

const fs = require('fs');
const IpfsApi = require('ipfs-http-client');
const OrbitDB = require('orbit-db');
const MongoClient = require('mongodb').MongoClient;
const createHash = require('hash-generator');
const ipfs = IpfsApi({host: IPFS_NODE, port: '5001', protocol: 'http'});
const msgpack = require("msgpack-lite");
const keypair = require("keypair");
const crypto = require("crypto");

(async () => {
    try {
        console.log(`Starting ipfs node`);
        // const ipfs = await IPFS.create(CONF);
        console.log('Setting up node..');
        const chunkGen = (_movies, l) => {
            return new Array(Math.ceil(_movies.length / l)).fill(0)
                .map((_, n) => _movies.slice(n * l, n * l + l));
        }

        // Create OrbitDB instance
        const DB_NAME = SOURCE_DB;
        const orbitdb = await OrbitDB.createInstance(ipfs);
        const ACCOUNTS_SIZE = 5
        const DAG_LINKS_SIZE = 2

        // DB
        const db = await orbitdb.log(DB_MOVIES, {
            overwrite: RECREATE,
            localOnly: false,
            replicate: true,
            accessController: {
                write: [orbitdb.identity.id]
            }
        });
        // END DB

        if (!SKIP_CLIENTS) {
            // CLIENTS
            console.log('Saving clients..');
            fs.writeFileSync('clients', '');

            let leafNodes = {}
            let collectionChain = [];
            let dbAddr = db.address.toString();
            for (const roots of Array(DAG_LINKS_SIZE).keys()) {
                let clients = {}
                let hash = createHash(50);

                for (const client of Array(ACCOUNTS_SIZE).keys()) {
                    let pair = keypair(1024)
                    let id = createHash(10);
                    let toEncrypt = Buffer.from(dbAddr, 'utf8')
                    let enCrypted = crypto.publicEncrypt(pair.public, toEncrypt).toString('base64')
                    collectionChain.push(`${id}.${hash}\n${pair.private}\n\n`)

                    // Merge clients
                    clients = {
                        ...clients, ...{
                            [id]: {key: enCrypted}
                        }
                    }
                }

                leafNodes = {
                    ...leafNodes, ...{
                        [hash]: await ipfs.dag.put({
                            keys: clients
                        }, {pin: true})
                    }
                };
            }

            let rootNode = await ipfs.dag.put({
                links: leafNodes,
                timestamp: Date.now(),
                size: ACCOUNTS_SIZE,
                childs: DAG_LINKS_SIZE
            }, {pin: true})

            // Testing dag links
            let testKey = Object.keys(leafNodes)[0]
            console.log(await ipfs.dag.get(rootNode, {
                path: `links/${testKey}/keys/`
            }));

            // Hold base hash
            let clientAddr = rootNode.toString();
            fs.writeFileSync('hash', dbAddr.split('/')[2]);
            // Save clients in file
            for (const chain of collectionChain) // Append client data
                fs.appendFileSync('clients', `${clientAddr}.${chain}`);

        }

        console.log('Starting db..');
        console.log(db.address.toString());
        db.events.on('peer', (p) => console.log('Peer Db:', p));

        // MOVIES
        let index = 0;
        const url = `mongodb:${MONGO_DB}//27017`;
        const client = new MongoClient(url);
        await client.connect(async () => {
            // Generate cursor for all movies
            const adminDb = client.db(DB_NAME)
            await adminDb.executeDbAdminCommand({setParameter: 1, internalQueryExecMaxBlockingSortBytes: 1048576000});
            const cursor = adminDb.collection('movies').find({}).limit(0).sort({year: 1})
            const size = await cursor.count();
            const data = chunkGen(await cursor.toArray(), MAX_CHUNKS);
            console.log('Total movies:', size)

            for (const chunk of data) {
                console.log('Starting');
                console.log('Chunk size:', chunk.length)

                let before = +new Date();
                let ch = chunk.map((v) => {
                    index++;
                    v['_id'] = `wt_loc_${index}`;
                    v['total'] = size;
                    v['small_cover_image'] = v['small_cover_image'].replace(/^.*\/\/[^\/]+/, '');
                    v['large_cover_image'] = v['large_cover_image'].replace(/^.*\/\/[^\/]+/, '');
                    v['medium_cover_image'] = v['medium_cover_image'].replace(/^.*\/\/[^\/]+/, '');

                    if ('torrents' in v) {
                        for (const value of v.torrents) {
                            delete value['url'];
                        }
                    }

                    delete v['background_image']
                    delete v['background_image_original']
                    delete v['summary']
                    delete v['synopsis']
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

                // console.log(cid);
                await db.add(cid.cid);
                console.log('Saving data..');
                console.log('Processed: ', `${index}/${size}`);
                console.log('Last id:', index);
                console.log('Memory:', (process.memoryUsage().heapUsed / 1024 / 1024).toFixed(2), 'Mb');
                console.log('Time Elapsed:', (+new Date() - before) / 1000 | 0);
                console.log('Created: ', cid.cid.toString());
            }

            await client.close();
            console.log('Closed db..');
        });

    } catch (err) {
        console.log(err);
    }

})()
