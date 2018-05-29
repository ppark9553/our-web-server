const redis = require('redis')

const GOBBLE_IP = '45.77.134.175'


class RedisClient {

  constructor() {
    console.log('Connecting to cache server (Redis) on Gobble server')
    this.redisClient = redis.createClient(6379, GOBBLE_IP)

    // redis client event handlers
    this.redisClient.on('connect', () => {
      console.log('Redis client connected')
    })

    this.redisClient.on('error', error => {
      console.log(`Something went wrong: ${error}`)
    })
  }

  async keyExists(key) {
    await this.redisClient.exists(key, (error, reply) => {
      if (!error) {
        if (reply === 1) {
         console.log('key exists')
        } else {
         console.log('key does not exist')
        }
      } else {
        console.log('there was an error with Redis while checking if key exists')
      }
    })
  }

  delKey(key) {
    this.redisClient.del(key, (error, reply) => {
      if (!error) {
        if (reply === 1) {
         console.log("key deleted");
        } else {
         console.log("key doesn't exist");
        }
      } else {
        console.log('there was an error with Redis while deleting key')
      }
    })
  }

  saveList(data) {
    console.log('Saving list/array data to Redis')
    this.redisClient.rpush(data, (error, reply) => {
      if (error) {
        console.log(error)
      } else {
        console.log(reply)
      }
    })
  }

  end() {
    console.log('Disconnecting Redis client')
    this.redisClient.quit()
  }

}

module.exports = {
  RedisClient: RedisClient
}
