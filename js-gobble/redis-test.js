const redis = require('redis')

const redis_client = redis.createClient(6379, '45.77.134.175')

redis_client.on('connect', () => {
    console.log('Redis client connected')
})

redis_client.on('error', error => {
    console.log('Something went wrong ' + error)
})

// redis_client.set('node_test_key', 'node_test_value', redis.print)
// redis_client.get('python_test_key', (error, result) => {
//     if (error) {
//         console.log(error);
//         throw error;
//     }
//     console.log('GET result -> ' + result);
// });

redis_client.lrange('mass_date', 0, -1, function(err, reply) {
    console.log(reply); // ['angularjs', 'backbone']
});
