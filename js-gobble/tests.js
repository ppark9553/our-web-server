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


///////////////////////////////////////////
const runTests = async () => {
  await testLogger()
  console.log('-----------------')
  await testFnguide()
  console.log('-----------------')
  console.log('Total tests: ' + totalTests)
  console.log('Test passed: ' + testPassed)
}

runTests()
