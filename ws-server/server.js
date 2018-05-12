var io = require('socket.io').listen(3000)
var pg = require ('pg')

var con_string = 'tcp://arbiter:makeitpopweAR!1@45.32.59.138/arbiter'

var pg_client = new pg.Client(con_string)
pg_client.connect()
var query = pg_client.query('LISTEN "projectstate"')

io.sockets.on('connection', function (socket) {
    socket.emit('connected', { connected: true })

    socket.on('ready for data', function (data) {
        pg_client.on('notification', function(id) {
            socket.emit('update', { message: id })
        })
    })
})
