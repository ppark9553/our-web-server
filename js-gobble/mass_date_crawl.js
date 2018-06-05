const Logger = require('./logger.js')
const Cache = require('./cache.js')
const Fnguide = require('./fnguide.js')
const Processor = require('./processor.js')

const main = async () => {
  // 1. define task_name, logger
  // 2. start fnguide puppet
  // 3. login to fnguide as user
  // 4. get mass date API
  // 5. save list data to cache
  // 6. send data save task to gateway server

  let task_name = 'MASS_DATE_CRAWL'
  let logger = new Logger.Logger()

  // log start process
  await logger.setLog(task_name, 'P', 'starting MASS_DATE_CRAWL.js script')

  // process
  let fn = new Fnguide.Puppet(task_name)
  await fn.logInitialized()
  await fn.startBrowser(false, 100)
  .then( response => { console.log(response) })
  .catch( error => { console.log(error) })
  await fn.login()
  let dateData = await fn.massDateCrawl()
  await fn.done()
  await logger.setLog(task_name, 'P', 'crawled dates data')

  let p = new Processor.Processor(dateData)
  let datesData = await p.processMassDate()
  await logger.setLog(task_name, 'P', 'processed dates data')

  let c = Cache.RedisClient()
  await c.setList(datesData)
  await c.end()
  await logger.setLog(task_name, 'P', 'dates data saved to cache')

  // log end process
  await logger.setLog(task_name, 'P', 'ran MASS_DATE_CRAWL.js successfully')
}

// run the main function
main()
