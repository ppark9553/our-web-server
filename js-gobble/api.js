const axios = require('axios')

const CONFIG = require('./config.js')
const GATEWAY_IP = CONFIG.ip.gateway


class API {

  constructor() {
    this.datesAPI = 'http://' + GATEWAY_IP + '/hidden-api/date/'
  }

  async getDates() {
    return axios.get(this.datesAPI)
  }

}

module.exports = {
  API: API
}
