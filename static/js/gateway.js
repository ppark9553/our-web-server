WEB_SOCKET_SWF_LOCATION = 'inc/WebSocketMain.swf'

// connect to socket.io server (gateway server)
var socket = io.connect('http://108.61.161.113:3000')
socket.on('connected', function (data) {
    if (data.connected == true) {
      console.log('webpage ready to load with changes in DB')
    }
    socket.emit('ready for data', {})
})
socket.on('update', function (data) {
    console.log('project state updated')
    console.log(data.message.payload)
})
