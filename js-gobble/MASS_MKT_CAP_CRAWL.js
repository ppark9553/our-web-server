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

  let taskName = 'MASS_MKT_CAP_CRAWL'
  let logger = new Logger.Logger()
  let taskSender = new TaskSender.TaskSender(taskName)

  // log start process
  await logger.setLog(taskName, 'P', 'starting MASS_DATE_CRAWL.js script')

  // process


  // log end process
  await logger.setLog(taskName, 'P', 'ran MASS_DATE_CRAWL.js successfully')
}

// run the main function
main()
