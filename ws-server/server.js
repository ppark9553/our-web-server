var io = require('socket.io').listen(3000)
var pg = require ('pg')

// connect to DB server PostgresSQL database
// DB server IP: 45.77.134.175
var con_string = 'tcp://arbiter:makeitpopwe123arBITER!1@45.77.134.175/arbiter'

var pg_client = new pg.Client(con_string)
pg_client.connect()

// start listening to database channel
// the channel name is "gatewaystate"
var query = pg_client.query('LISTEN "gatewaystate"')

// EVENT: "connection" -- socket.io
io.sockets.on('connection', function (socket) {
    // handle socket.io events here
    // connection has succeeded once you are in here

    // CLIENT EVENT 1: "connected"
    socket.emit('connected', { connected: true })

    // SERVER EVENT 1: "reday for data" -- socket.io
    socket.on('ready for data', function (data) {

        // SERVER EVENT 2: "notification" -- pg
        pg_client.on('notification', function (id) {
            // CLIENT EVENT 2: "update"
            socket.emit('update', { message: id })
        })
    })
})
