const fs = require('fs');
const NodeRSA = require('node-rsa');
const rootKeys = `keys/`

const keyPair = {
    encrypt(pubKey, data) {
        const key = new NodeRSA(pubKey)
        return key.encrypt(data, 'hex')
    },
    decrypt(pvtKey, data) {
        const key = new NodeRSA(pvtKey)
        return key.decrypt(Buffer.from(data))
    },
    private(client) {
        return fs.readFileSync(`${rootKeys}/${client}/private.key`)
    },
    public(client) {
        return fs.readFileSync(`${rootKeys}/${client}/public.key`)
    },
    keygen: (client) => {
        let key = new NodeRSA({b: 1024});
        let path = `${rootKeys}/${client}/`
        let privpem = key.exportKey('pkcs8-private-pem')
        let pubpem = key.exportKey('pkcs8-public-pem')

        if (!fs.existsSync(path))
            fs.mkdirSync(path, {recursive: true})


        let publicPath = `${path}public.key`
        let privatePath = `${path}private.key`
        fs.writeFileSync(publicPath, Buffer.from(pubpem))
        fs.writeFileSync(privatePath, Buffer.from(privpem))
        return [publicPath, privatePath]

    }
}

module.exports = keyPair