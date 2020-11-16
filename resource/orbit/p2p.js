'use strict'

const Libp2p = require('libp2p')
const TCP = require('libp2p-tcp')
const wrtc = require('wrtc')
const Websockets = require('libp2p-websockets')
const WebrtcStar = require('libp2p-webrtc-star')
const Bootstrap = require('libp2p-bootstrap')
const Gossipsub = require('libp2p-gossipsub')
const KadDHT = require('libp2p-kad-dht')
const MPLEX = require('libp2p-mplex')
const SECIO = require('libp2p-secio')
const {FaultTolerance} = require('libp2p/src/transport-manager');

module.exports = (opts) => {
	// Set convenience variables to clearly showcase some of the useful things that are available
	const peerId = opts.peerId;
	const bootstrapList = opts.config.Bootstrap;
	
	// Build and return our libp2p node
	const p2p = new Libp2p({
		peerId,
		addresses: {
			listen: [
				'/ip4/0.0.0.0/tcp/4005',
				'/ip4/0.0.0.0/tcp/4006/ws',
				'/dns4/secure-beyond-12878.herokuapp.com/tcp/443/wss/p2p-webrtc-star/',
				'/dns4/wrtc-star1.par.dwebops.pub/tcp/443/wss/p2p-webrtc-star/',
				'/dns4/wrtc-star2.sjc.dwebops.pub/tcp/443/wss/p2p-webrtc-star/'
			]
		},
		transportManager: {
			faultTolerance: FaultTolerance.NO_FATAL
		},
		// Lets limit the connection managers peers and have it check peer health less frequently
		modules: {
			transport: [TCP, Websockets, WebrtcStar],
			streamMuxer: [MPLEX],
			connEncryption: [SECIO],
			peerDiscovery: [Bootstrap],
			dht: KadDHT,
			pubsub: Gossipsub
		},
		config: {
			transport: {
				[WebrtcStar.prototype[Symbol.toStringTag]]: {
					wrtc
				}
			},
			peerDiscovery: {
				autoDial: true,
				websocketStar: {
					enabled: false
				},
				webRTCStar: {
					enabled: true
				},
				bootstrap: {
					enabled: true,
					list: bootstrapList
				}
			},
			pubsub: {
				enabled: true,
				emitSelf: true
			},
			dht: {
				kBucketSize: 20,
				enabled: false,
				randomWalk: {
					enabled: false
				}
			}
		}
	})
	
	// p2p.connectionManager.on('peer:connect', (connection) => {
	// 	console.log('Connection established to:', connection.remotePeer.toB58String())	// Emitted when a new connection has been created
	// })
	//
	// p2p.on('peer:discovery', (peerId) => {
	// 	// No need to dial, autoDial is on
	// 	console.log('Discovered:', peerId.toB58String())
	// })
	
	return p2p
}
