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

  let taskName = 'MASS_SD_CRAWL'
  let logger = new Logger.Logger()
  let taskSender = new TaskSender.TaskSender(taskName)
  let api = new API.API()

  // log start process
  await logger.setLog(taskName, 'P', 'starting MASS_SD_CRAWL.js script')

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

  // retrieve dates first
  let datesData = await api.retrieveAllDates()
  for (let date of datesData) {
    // loop through all the dates and start crawling data
    let sdData = await fn.massSDCrawl(date)
    let p = new Processor.Processor(sdData)
    let allSdData = await p.processMassSD(date)
    console.log(allSdData)

    // connect to cache and save data
    let c = new Cache.RedisClient()
    await c.auth()
    let keyExists = await c.keyExists('mass_sd') // first delete key if already existent
    if (keyExists == 1) {
      await c.delKey('mass_sd')
    }
    await c.setList(allSdData)
    console.log('cache set complete')

    // after setting mass_sd to cache, set the mass_sd_date key value
    let dateKeyExists = await c.keyExists('mass_sd_date')
    if (dateKeyExists == 1) {
      await c.delKey('mass_sd_date')
    }
    await c.setKey('mass_sd_date', date)
    console.log('set date cache key complete')

    // send new task to gateway server: MASS_SD_SAVE
    await taskSender.sendTask('MASS_SD_SAVE')

    // after set cache, poll django for save to DB complete event
    // once Django app has saved all the cached data, start with the next date

    // first loop until key exists
    // this is because when this program is ran for the first tiem,
    // the key will not exist
    let savedCompleteKeyExists = await c.keyExists('mass_sd_state')
    while (savedCompleteKeyExists != 1) {
      savedCompleKeyExists = await c.keyExists('mass_sd_state')
    }
    // proceed with polling when the key exists
    if (savedCompleKeyExists == 1) {
      // check that the state's value is crawl and not save
      // if the state is 'save', that means that Django is still in the process of saving data
      let savedComplete = await c.getKey('mass_sd_state')
      while (savedComplete != 'crawl') {
        savedComplete = await c.getKey('mass_sd_state')
      }
    } // once you are out of this block, the polling is complete
    
  } // loop ends here //
  await fn.done()

  // log end process
  await logger.setLog(taskName, 'P', 'ran MASS_SD_CRAWL.js successfully')
}

// run the main function
main()
