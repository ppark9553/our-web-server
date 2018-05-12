const puppeteer = require('puppeteer');

String.prototype.format = function() {
  // es5 syntax function
  // finds '{}' within string values and replaces them with
  // given parameter values in the .format method
  var formatted = this
  for (var i = 0; i < arguments.length; i++) {
      var regexp = new RegExp('\\{'+i+'\\}', 'gi')
      formatted = formatted.replace(regexp, arguments[i])
  }
  return formatted;
}

// define page and browser variables for firing up chrome
let page
let browser
// width and height definitions for non-headless mode
const width = 1920
const height = 1080

// define all the api endpoints here
const LOGIN_PAGE = 'https://www.fnguide.com/home/login'
// user info object here
const USER = {
  'id': 'flex80',
  'pw': '80_sangbum'
}
const API = {
  'date': 'http://www.fnguide.com/api/Fgdd/StkIndMByTimeGrdData?IN_MULTI_VALUE=CJA005930%2CCII.001&IN_START_DT=20000101&IN_END_DT={0}&IN_DATE_TYPE=D&IN_ADJ_YN=Y&_=1525866864922',
  'market_cap': 'http://www.fnguide.com/api/Fgdd/StkItemDateCapGrdDataDate?IN_MKT_TYPE=0&IN_SEARCH_DT={0}&_=1525867541072',
  'sd': 'http://www.fnguide.com/Api/Fgdd/StkJInvTrdTrendGrdDataDate?IN_MKT_TYPE=0&IN_TRD_DT={0}&IN_UNIT_GB=2&_=1525867599123',
  'short': 'http://www.fnguide.com/Api/Fgdd/StkLendingGrdDataDateC?IN_MKT_GB=0&IN_STD_DT={0}&IN_DATA_GB=D&_=1525867734721',
  'financial': 'http://www.fnguide.com/api/Fgdd/StkDateShareIndxGrdDataDate?IN_SEARCH_DT={0}&IN_MKT_TYPE=0&IN_CONSOLIDATED=1&_=1525867857090',
  'etf': 'http://www.fnguide.com/Api/Fgdd/StkEtfGrdDataDate?IN_TRD_DT={0}&IN_MKT_GB=0&_=1525867906347'
}

// create a function for scraping all data from 20000101 to today date
const scrape_all = async () => {
  let today_date = new Date().toISOString().slice(0, 10).replace(/-/gi, '')
  console.log(`Today date: ${today_date}`)

  console.log('Crawling FnGuide starting...')

  browser = await puppeteer.launch({
    headless: false,
    slowMo: 80,
    args: ['--window-size=${width}, ${height}']
  })
  page = await browser.newPage()
  await page.setViewport({ width, height })

  // go to login page and login
  const id_input_selector = '#txtID'
  const pw_input_selector = '#txtPW'
  const login_btn_selector = '#container > div > div > div.log--wrap > div.log--area > form > div > fieldset > button'
  const logout_other_ip_user_btn_selector = '#divLogin > div.lay--popFooter > form > button.btn--back'
  const user_id_selector = 'body > div.header > div > div.util > p > span:nth-child(1)'
  await page.goto(LOGIN_PAGE)
  await page.waitForSelector(id_input_selector)
  await page.click(id_input_selector)
  await page.type(id_input_selector, USER.id)
  await page.click(pw_input_selector)
  await page.type(pw_input_selector, USER.pw)
  await page.click(login_btn_selector)

  const logout_other_ip_user_btn_exists = await page.$eval(
    logout_other_ip_user_btn_selector,
    el => (el ? true : false)
  )
  if (logout_other_ip_user_btn_exists) {
    await page.click(logout_other_ip_user_btn_selector)
  }

  await page.waitForSelector(user_id_selector)
  // user login complete
  // now, scrape whatever data you want on FnGuide

  return true
}

// run program here
scrape_all().then((status) => {
  if (status == true) {
    console.log('scrape complete')
  } else {
    console.log('scrape failed')
  }
})
