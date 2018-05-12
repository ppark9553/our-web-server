import puppeteer from 'puppeteer'

let page
let browser
const width = 1920
const height = 1080

const LOGIN_PAGE = 'https://www.fnguide.com/home/login'
const MARKET_CAP_PAGE = 'http://www.fnguide.com/fgdd/StkItemDateCap#tab=D&market=0'
const FN_ID = 'flex80'
const FN_PW = '80_sangbum'

beforeAll(async () => {
  browser = await puppeteer.launch({
    headless: false,
    slowMo: 80,
    args: ['--window-size=${width}, ${height}']
  })
  page = await browser.newPage()
  await page.setViewport({ width, height })
})

afterAll(() => {
  // pass
})

describe('login page', () => {

  test('can go to login page', async () => {
    const page_title_selector = '#container > div > div > div.log--wrap > div.grid--header.mem > div'
    await page.goto(LOGIN_PAGE)
    await page.waitForSelector(page_title_selector)
    const page_title = await page.$eval(page_title_selector, el => el.innerText)
    expect(page_title).toBe('회원 로그인')
  }, 16000)

  test('can fill in login form and login', async () => {
    const id_input_selector = '#txtID'
    const pw_input_selector = '#txtPW'
    const login_btn_selector = '#container > div > div > div.log--wrap > div.log--area > form > div > fieldset > button'
    const logout_other_ip_user_btn_selector = '#divLogin > div.lay--popFooter > form > button.btn--back'
    const user_id_selector = 'body > div.header > div > div.util > p > span:nth-child(1)'
    await page.goto(LOGIN_PAGE)
    await page.waitForSelector(id_input_selector)
    await page.click(id_input_selector)
    await page.type(id_input_selector, FN_ID)
    await page.click(pw_input_selector)
    await page.type(pw_input_selector, FN_PW)
    await page.click(login_btn_selector)

    const logout_other_ip_user_btn_exists = await page.$eval(
      logout_other_ip_user_btn_selector,
      el => (el ? true : false)
    )
    if (logout_other_ip_user_btn_exists) {
      await page.click(logout_other_ip_user_btn_selector)
    }

    await page.waitForSelector(user_id_selector)
    const user_id = await page.$eval(user_id_selector, el => el.innerText)
    let user_id_correct = user_id.includes(FN_ID)
    expect(user_id_correct).toBe(true)
  }, 16000)

})

describe('fnguide date', () => {

  test('can get data through pure API request', async () => {
    // first get today's date
    let today_date = new Date().toISOString().slice(0, 10).replace('-', '')
    // testing to see if we can reset or add key values to request headers: IT WORKS
    await page.setExtraHTTPHeaders({
      'Referer': 'http://www.fnguide.com/fgdd/StkItemDateCap',
      'X-Requested-With': 'XMLHttpRequest'
    })
    let get_date_api_url = `http://www.fnguide.com/api/Fgdd/StkIndMByTimeGrdData?IN_MULTI_VALUE=CJA005930%2CCII.001&IN_START_DT=20000101&IN_END_DT=${today_date}&IN_DATE_TYPE=D&IN_ADJ_YN=Y&_=1525865507542`
    await page.goto(get_date_api_url)
  }, 16000)

})

// describe('market cap page', () => {
//
//   test('can get data through pure API request', async () => {
//     await page.setExtraHTTPHeaders({
//       'Referer': 'http://www.fnguide.com/fgdd/StkItemDateCap',
//       'X-Requested-With': 'XMLHttpRequest'
//     })
//     let market_cap_api_url = 'http://www.fnguide.com/api/Fgdd/StkItemDateCapGrdDataDate?IN_MKT_TYPE=0&IN_SEARCH_DT=20180508&_=1525863542903'
//     await page.goto(market_cap_api_url)
//   }, 16000)
//
// })
