const io = require('socket.io').listen(3000)
const pg = require ('pg')

const con_string = 'tcp://arbiter:makeitpopweAR!1@445.77.134.175/arbiter'

let pg_client = new pg.Client(con_string)
pg_client.connect()
let query = pg_client.query('LISTEN "projectstate"')

io.sockets.on('connection', socket => {
    socket.emit('connected', { connected: true })

    socket.on('ready for data', data => {
        pg_client.on('notification', id => {
            socket.emit('update', { message: id })
        })
    })
})
