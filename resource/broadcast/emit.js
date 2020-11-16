const WStar = require('libp2p-webrtc-star')
const multiaddr = require('multiaddr')
const pipe = require('it-pipe')
const electronWebRTC = require('electron-webrtc')
const {collect} = require('streaming-iterables')

(async () => {
	
	const nodeId = '8bkinn8owtxcrsvqpx6v0elyanmmr3f4r16wstgbbn5ulw8h53'
	const addr = multiaddr(`/ip4/188.166.203.82/tcp/20000/wss/p2p-webrtc-star/p2p/${nodeId}`)
	const ws = new WStar({wrtc: electronWebRTC()})
	
	const listener = ws.createListener((socket) => {
		console.log('new connection opened')
		pipe(['hello'], socket)
	})
	
	await listener.listen(addr)
	console.log('listening')
	
	
	
})()