const wrtc = require('wrtc')
const WebRTCStar = require('libp2p-webrtc-star');
const KadDHT = require('libp2p-kad-dht');
const Libp2p = require('libp2p');
const TCP = require('libp2p-tcp')
const PeerInfo = require('peer-info')



async function start(){
	const node = await Libp2p.create({
		modules: {
			transport: [TCP]
		}
	})
	
	console.log(node);
}

start();