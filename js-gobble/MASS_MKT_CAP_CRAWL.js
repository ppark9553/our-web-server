const Logger = require('./logger.js')
const Cache = require('./cache.js')
const Fnguide = require('./fnguide.js')
const API = require('./api.js')
const Processor = require('./processor.js')
const TaskSender = require('./taskSender.js')

const main = async () => {
  // 1. define task_name, logger
  // 2. start fnguide puppet
  // 3. login to fnguide as user
  // 4. check the dates in database, return them as a list to loop over
  // 5. starting from the most recent date, start scraping
  // 6. get market cap API by date
  // 7. save json data to cache
  // 8. send data save task to gateway server

  let taskName = 'MASS_MKT_CAP_CRAWL'
  let logger = new Logger.Logger()
  let taskSender = new TaskSender.TaskSender(taskName)
  let api = new API.API()

  // log start process
  await logger.setLog(taskName, 'P', 'starting MASS_DATE_CRAWL.js script')

  // process
  let fn = new Fnguide.Puppet(taskName)
  await fn.logInitialized()
  await fn.startBrowser(false, 100)
  .then( response => { console.log(response) })
  .catch( error => { console.log(error) })
  await fn.login()
  .then( response => {
    // pass
  })
  .catch( error => {
    logger.setLog(taskName, 'F', 'user login failed, retrying login')
    fn.login()
  })
  // browser load complete, and logged in
  await logger.setLog(taskName, 'p', 'retrieving all dates crawler needs to crawl')
  let datesData = await api.retrieveAllDates()
  for (let date of datesData) {
    let mktCapData = await fn.massMktCapCrawl(date)
    console.log(mktCapData)
    break
  }

  // log end process
  await logger.setLog(taskName, 'P', 'ran MASS_DATE_CRAWL.js successfully')
}

// run the main function
main()
