const Logger = require('./logger.js')
const Fnguide = require('./fnguide.js')
const Processor = require('./processor.js')
const Cache = require('./cache.js')

let totalTests = 0
let testPassed = 0

// logger test
async function testLogger() {
  totalTests += 1
  let logger = new Logger.Logger()
  console.log(logger.logURL)
  console.log(logger.date)

  let taskName = 'test task'
  let state = 'P'
  let log = 'testing logger'

  await logger.setLog(taskName, state, log)

  testPassed += 1
}

// fnguide test
async function testFnguide() {
  totalTests += 1
  let fn = new Fnguide.Puppet('fnguide_test')
  await fn.logInitialized()
  console.log('1. fn initialized')
  await fn.startBrowser(false, 100)
  console.log('2. started browser')
  await fn.login()
  console.log('3. logged in')
  let dateData = await fn.massDateCrawl()
  console.log('4. date data received')
  let p = new Processor.Processor(dateData)
  let datesData = await p.processMassDate()
  console.log('5. processed data')
  let c = new Cache.RedisClient()
  await c.delKey('mass_date')
  await c.saveList(datesData)
  await c.end()
  console.log('6. saved data to cache')
  await fn.done()
  console.log('6. closing browser')

  testPassed += 1
}

async function testCache() {
  totalTests += 1
  let c = new Cache.RedisClient()

  // await c.saveList(['redis-tester', 1, 2, 3])

  let key = 'testcache'

  console.log('Test cache can set key')
  let status = await c.setKey(key, 'testing cache set key')
  console.log(status == true)
  console.log('==========')

  console.log('Test cache can get key')
  let response = await c.getKey(key)
  console.log(response == 'testing cache set key')
  console.log('==========')

  console.log('Test cache can check key existence')
  let exists = await c.keyExists(key)
  console.log(exists == 1)
  console.log('==========')

  console.log('Test cache can delete key')
  let r = await c.delKey(key)
  console.log(r == 1)
  console.log('==========')

  console.log('Test cache can set list value')
  // delete key if exists
  console.log('&& Test cache can check/delete list key')
  let listExists = await c.keyExists('listkey')
  if (listExists == 1) {
    console.log('listkey exists')
    let listr = await c.delKey('listkey')
    if (listr == 1) {
      console.log('deleted listkey')
    }
  } else {
    console.log('no existing key called listkey')
  }
  let listData = ['listkey', 1, 2, 3, 4]
  let list = await c.setList(listData)
  console.log(list == 4)
  console.log('==========')

  console.log('Test cache can get list key')
  let listResponse = await c.getList('listkey', 'int')
  console.log(listResponse)
  console.log('==========')

  console.log('Test cache can catch list error')
  let listExists2 = await c.keyExists('listkey2')
  if (listExists2 == 1) {
    console.log('listkey2 exists')
    let listr2 = await c.delKey('listkey2')
    if (listr2 == 1) {
      console.log('deleted listkey2')
    }
  } else {
    console.log('no existing key called listkey2')
  }
  let listData2 = ['listkey2', 'hello', 'there', 'peepee']
  let list2 = await c.setList(listData2)
  let listResponse2 = await c.getList('listkey2', 'int')
  console.log(listResponse2)
  console.log('==========')

  console.log('Test cache can set JSON')
  let json = {
    'key1': 1,
    'key2': 2,
    'complicatedKey': {
      'key1': 1,
      'key2': 2
    },
    'complicatedKey2': {
      'compKey1': 1,
      'compKey2': 2
    }
  }
  let jsonExists = await c.keyExists('jsontest')
  if (jsonExists == 1) {
    console.log('jsontest exists')
    let jsontest = await c.delJSON('jsontest')
    if (jsontest == 1) {
      console.log('deleted jsontest')
    }
  } else {
    console.log('no existing key called jsontest')
  }
  let jsonResponse = await c.setJSON('jsontest', json)
  console.log(jsonResponse == 1)
  console.log('==========')

  console.log('Test cache can get JSON')
  let retJSON = await c.getJSON('jsontest')
  console.log(retJSON)
  console.log('key1? ' + retJSON.key1)
  console.log('complicatedKey.key1? ' + retJSON.complicatedKey.key1)
  console.log('==========')

  await c.end()
  testPassed += 1
}


///////////////////////////////////////////
const runTests = async () => {
  // await testLogger()
  // console.log('-----------------')
  // await testFnguide()
  // console.log('-----------------')
  await testCache()
  console.log('-----------------')
  console.log('Total tests: ' + totalTests)
  console.log('Test passed: ' + testPassed)
}

runTests()
