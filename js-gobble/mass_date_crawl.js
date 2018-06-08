const Logger = require('./logger.js')
const Cache = require('./cache.js')
const Fnguide = require('./fnguide.js')
const Processor = require('./processor.js')
const TaskSender = require('./taskSender.js')

const main = async () => {
  // 1. define task_name, logger
  // 2. start fnguide puppet
  // 3. login to fnguide as user
  // 4. get mass date API
  // 5. save list data to cache
  // 6. send data save task to gateway server

  let taskName = 'MASS_DATE_CRAWL'
  let logger = new Logger.Logger()
  let taskSender = new TaskSender.TaskSender(taskName)

  // log start process
  await logger.setLog(taskName, 'P', 'starting MASS_DATE_CRAWL.js script')

  // process
  let fn = new Fnguide.Puppet(taskName)
  await fn.logInitialized()
  await fn.startBrowser(true, 100)
  .then( response => { console.log(response) })
  .catch( error => { console.log(error) })
  await fn.login()
  .then( response => {
    // pass
  })
  .catch( error => {
    await logger.setLog(taskName, 'F', 'user login failed, retrying login')
    fn.login()
  })
  let dateData = await fn.massDateCrawl()
  await fn.done()
  await logger.setLog(taskName, 'P', 'crawled dates data')

  let p = new Processor.Processor(dateData)
  let datesData = await p.processMassDate()
  await logger.setLog(taskName, 'P', 'processed dates data')

  let c = new Cache.RedisClient()
  await c.auth()
  await c.setList(datesData)
  await c.end()
  await logger.setLog(taskName, 'P', 'dates data saved to cache')

  await taskSender.sendTask('MASS_DATE_SAVE')
  await logger.setLog(taskName, 'P', 'sent MASS_DATE_SAVE action to gateway server')

  // log end process
  await logger.setLog(taskName, 'P', 'ran MASS_DATE_CRAWL.js successfully')
}

// run the main function
main()
