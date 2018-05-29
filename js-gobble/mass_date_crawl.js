const logger = require('./logger.js')
// const fnguide = require('./fnguide.js')
const fnguide = require('./fnguide.js')

String.prototype.format = function() {
  // finds '{}' within string values and replaces them with
  // given parameter values in the .format method
  var formatted = this
  for (var i = 0; i < arguments.length; i++) {
      var regexp = new RegExp('\\{'+i+'\\}', 'gi')
      formatted = formatted.replace(regexp, arguments[i])
  }
  return formatted
}

const API = {
  'date': 'http://www.fnguide.com/api/Fgdd/StkIndMByTimeGrdData?IN_MULTI_VALUE=CJA005930%2CCII.001&IN_START_DT=20000101&IN_END_DT={0}&IN_DATE_TYPE=D&IN_ADJ_YN=Y&_=1525866864922',
  'market_cap': 'http://www.fnguide.com/api/Fgdd/StkItemDateCapGrdDataDate?IN_MKT_TYPE=0&IN_SEARCH_DT={0}&_=1525867541072',
  'sd': 'http://www.fnguide.com/Api/Fgdd/StkJInvTrdTrendGrdDataDate?IN_MKT_TYPE=0&IN_TRD_DT={0}&IN_UNIT_GB=2&_=1525867599123',
  'short': 'http://www.fnguide.com/Api/Fgdd/StkLendingGrdDataDateC?IN_MKT_GB=0&IN_STD_DT={0}&IN_DATA_GB=D&_=1525867734721',
  'financial': 'http://www.fnguide.com/api/Fgdd/StkDateShareIndxGrdDataDate?IN_SEARCH_DT={0}&IN_MKT_TYPE=0&IN_CONSOLIDATED=1&_=1525867857090',
  'etf': 'http://www.fnguide.com/Api/Fgdd/StkEtfGrdDataDate?IN_TRD_DT={0}&IN_MKT_GB=0&_=1525867906347'
}

const main = async () => {

  let task_name = 'mass_date_crawl'

  // log start process
  await logger.set_log(task_name, 'P', 'starting mass_date_crawl.js script')

  // process
  console.log('mass_date_crawl starting')
  let fn = new fnguide.Puppet()
  let page = fn.start_browser(false, 100)

  let today_date = new Date().toISOString().slice(0, 10).replace(/-/gi, '')
  await page.goto(API.date.format(today_date))

  // log end process
  await logger.set_log(task_name, 'P', 'ran mass_date_crawl.js successfully')

}

// run the main function
main()
