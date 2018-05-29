const cache = require('./cache.js')

const main = async () => {
  let c = new cache.RedisClient()

  await c.saveList(['redis-tester', 1, 2, 3])

  // await c.delKey('redis-tester')

  await c.keyExists('redis-tester')
  await console.log(c.exists)

  await c.end()
}

main()
