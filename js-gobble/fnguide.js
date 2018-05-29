const puppeteer = require('puppeteer')

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

  constructor() {
    // user id and pw
    this.id = 'flex80'
    this.pw = '80_sangbum'

    // width and height definitions for non-headless mode
    this.width = 1920
    this.height = 1080

    let today_date = new Date().toISOString().slice(0, 10).replace(/-/gi, '')
    console.log(`Today date: ${today_date}`)

    console.log('FnGuide puppet starting...')
  }

  async start_browser(headless_bool=true, slowMo_time=100) {
    let width = this.width
    let height = this.height

    // sets the browser attribute
    this.browser = await puppeteer.launch({
      headless: headless_bool,
      args: ['--no-sandbox'],
      slowMo: slowMo_time,
      args: ['--window-size=${width}, ${height}']
    })
    this.page = await this.browser.newPage()

    await this.page.setViewport({ width, height })
  }

  async goTo() {
    let page = this.page

    console.log(URL.LOGIN_PAGE)
    await page.goto(URL.LOGIN_PAGE)
  }

  async login() {
    // go to login page and login
    let page = this.page

    const id_input_selector = '#txtID'
    const pw_input_selector = '#txtPW'
    const login_btn_selector = '#container > div > div > div.log--wrap > div.log--area > form > div > fieldset > button'
    const logout_other_ip_user_btn_selector = '#divLogin > div.lay--popFooter > form > button.btn--back'
    const user_id_selector = 'body > div.header > div > div.util > p > span:nth-child(1)'
    await page.goto(LOGIN_PAGE)
    await page.waitForSelector(id_input_selector)
    await page.click(id_input_selector)
    await page.type(id_input_selector, this.id)
    await page.click(pw_input_selector)
    await page.type(pw_input_selector, this.pw)
    await page.click(login_btn_selector)

    const logout_other_ip_user_btn_exists = await page.$eval(
      logout_other_ip_user_btn_selector,
      el => (el ? true : false)
    )
    if (logout_other_ip_user_btn_exists) {
      await page.click(logout_other_ip_user_btn_selector)
      await page.waitForSelector(user_id_selector)
    } else {
      await page.waitForSelector(user_id_selector)
    }

    console.log('user logged in, ready to scrape data')
  }

}

module.exports = {
  Puppet: Puppet
}
