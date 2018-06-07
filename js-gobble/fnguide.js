const puppeteer = require('puppeteer')
const Logger = require('./logger.js')

String.prototype.format = function() {
  // es5 synatax
  // finds '{}' within string values and replaces them with
  // given parameter values in the .format method
  var formatted = this
  for (var i = 0; i < arguments.length; i++) {
      var regexp = new RegExp('\\{'+i+'\\}', 'gi')
      formatted = formatted.replace(regexp, arguments[i])
  }
  return formatted
}

// define all the api endpoints here
const URL = {
  'LOGIN_PAGE': 'https://www.fnguide.com/home/login',
  'DATE_PAGE': 'http://www.fnguide.com/fgdd/StkIndmByTime#multivalue=CJA005930|CII.001&adjyn=Y&multiname=삼성전자|종합주가지수',
  'MKTCAP_PAGE': 'http://www.fnguide.com/fgdd/StkItemDateCap#tab=D&market=0',
  'API': {
    'date': 'http://www.fnguide.com/api/Fgdd/StkIndMByTimeGrdData?IN_MULTI_VALUE=CJA005930%2CCII.001&IN_START_DT=20000101&IN_END_DT={0}&IN_DATE_TYPE=D&IN_ADJ_YN=Y&_=1525866864922',
    'market_cap': 'http://www.fnguide.com/api/Fgdd/StkItemDateCapGrdDataDate?IN_MKT_TYPE=0&IN_SEARCH_DT={0}&_=1525867541072',
    'sd': 'http://www.fnguide.com/Api/Fgdd/StkJInvTrdTrendGrdDataDate?IN_MKT_TYPE=0&IN_TRD_DT={0}&IN_UNIT_GB=2&_=1525867599123',
    'short': 'http://www.fnguide.com/Api/Fgdd/StkLendingGrdDataDateC?IN_MKT_GB=0&IN_STD_DT={0}&IN_DATA_GB=D&_=1525867734721',
    'financial': 'http://www.fnguide.com/api/Fgdd/StkDateShareIndxGrdDataDate?IN_SEARCH_DT={0}&IN_MKT_TYPE=0&IN_CONSOLIDATED=1&_=1525867857090',
    'etf': 'http://www.fnguide.com/Api/Fgdd/StkEtfGrdDataDate?IN_TRD_DT={0}&IN_MKT_GB=0&_=1525867906347'
  }
}


class Puppet {

  constructor(taskName) {
    // always start the logger first
    // log every process you do so you can check it from the gateway webpage
    this.logger = new Logger.Logger()
    this.taskName = taskName

    // user id and pw
    this.id = 'flex80'
    this.pw = '80_sangbum'

    // width and height definitions for non-headless mode
    this.width = 1920
    this.height = 1080

    this.todayDate = new Date().toISOString().slice(0, 10).replace(/-/gi, '')
  }

  async logInitialized() {
    // log that you have successfully started Puppeteer
    await this.logger.setLog(this.taskName, 'P', 'Today date: ' + this.todayDate)
    await this.logger.setLog(this.taskName, 'P', 'FnGuide puppet starting...')
  }

  async startBrowser(headless_bool=true, slowMo_time=100) {
    // set attribute values to local variables for ease of use
    let width = this.width
    let height = this.height

    // sets the browser attribute
    if (headless_bool == true) {
      var puppeteerConfig = {
        headless: headless_bool,
        args: ['--no-sandbox'],
        slowMo: slowMo_time,
      }
    } else if (headless_bool = false) {
      var puppeteerConfig = {
        headless: headless_bool,
        args: ['--no-sandbox'],
        slowMo: slowMo_time,
        args: ['--window-size=${width}, ${height}']
      }
    }
    this.browser = await puppeteer.launch(puppeteerConfig)
    this.page = await this.browser.newPage()

    await this.page.setViewport({ width, height })
    await this.logger.setLog(this.taskName, 'P', 'Puppeteer browser ready to gobble data')
  }

  async login() {
    // go to login page and login
    let page = this.page

    const IDInputSelector = '#txtID'
    const PWInputSelector = '#txtPW'
    const loginBtnSelector = '#container > div > div > div.log--wrap > div.log--area > form > div > fieldset > button'
    const logoutOtherIPUserBtnSelector = '#divLogin > div.lay--popFooter > form > button.btn--back'
    const FnguideLogoSelector = 'body > div.header > div > h1 > a'
    // const userIDSelector = 'body > div.header > div > div.util > p > span:nth-child(1)'
    await page.goto(URL.LOGIN_PAGE)
    await page.waitForSelector(IDInputSelector)
    await page.click(IDInputSelector)
    await page.type(IDInputSelector, this.id)
    await page.click(PWInputSelector)
    await page.type(PWInputSelector, this.pw)
    await page.click(loginBtnSelector)

    const logoutOtherIPUserBtnExists = await page.$eval(
      logoutOtherIPUserBtnSelector,
      el => (el ? true : false)
    )
    if (logoutOtherIPUserBtnExists) {
      await page.click(logoutOtherIPUserBtnSelector)
    }

    // issues with waitForSelector
    // force wait for 5 seconds before waitForSelector
    // initially waited for userIDSelector but didn't work
    // so now waiting for FnguideLogoSelector
    await page.waitForSelector(FnguideLogoSelector)
    // await page.waitForSelector(userIDSelector)

    await this.logger.setLog(this.taskName, 'P', 'User logged in, ready to gobble')
  }

  async massDateCrawl() {
    let page = this.page

    // set headers to fool Fnguide
    await page.setExtraHTTPHeaders({
      'Referer': 'http://www.fnguide.com/fgdd/StkIndmByTime',
      'X-Requested-With': 'XMLHttpRequest'
    })
    let dateURL = URL.API.date.format(this.todayDate)
    await page.goto(dateURL)
    const dateData = await page.evaluate(() => {
        let data = JSON.parse(document.querySelector('body').innerText)
        return data
    })

    return dateData
  }

  async done() {
    await this.browser.close()
    await this.logger.setLog(this.taskName, 'P', 'Gobbling complete, Puppeteer browser closed')
  }

}

module.exports = {
  Puppet: Puppet
}
