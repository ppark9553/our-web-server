const axios = require('axios')

const CONFIG = require('./config.js')
const GATEWAY_IP = CONFIG.ip.gateway


class API {

  constructor() {
    this.datesAPI = 'http://' + GATEWAY_IP + '/hidden-api/date/?page='
  }

  async getDates(pageNum, url=false) {
    let fullDatesAPI = ''
    if (url == false) {
      fullDatesAPI = this.datesAPI + pageNum
    } else {
      fullDatesAPI = url
    }
    return axios.get(fullDatesAPI)
  }

  async retrieveAllDates() {
    let datesData = await this.getDates(1, false)
    let nextURL = datesData.data.next
    let datesDataResult = datesData.data.results
    let allDates = []
    while (nextURL != null) {
      for (let dateData of datesDataResult) {
        let dateDataPoint = dateData.date
        allDates.push(dateDataPoint)
      }
      let datesData = await this.getDates(0, nextURL)
      nextURL = datesData.data.next
      datesDataResult = datesData.data.results
    }
    return allDates
  }

}

module.exports = {
  API: API
}
