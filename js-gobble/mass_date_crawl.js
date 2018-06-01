const Logger = require('./logger.js')
const Cache = require('./cache.js')
const Fnguide = require('./fnguide.js')

const main = async () => {

  let task_name = 'MASS_DATE_CRAWL'
  let logger = new Logger.Logger()

  // log start process
  await logger.setLog(task_name, 'P', 'starting MASS_DATE_CRAWL.js script')

  // process
  console.log('mass_date_crawl starting')
  let fn = new Fnguide.Puppet(task_name)
  fn.start_browser(false, 100)
    .then( status => { console.log(status) })
    .catch( error => { console.log(error) })

  // log end process
  await logger.setLog(task_name, 'P', 'ran MASS_DATE_CRAWL.js successfully')

}

// run the main function
main()
