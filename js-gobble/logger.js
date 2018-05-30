const axios = require('axios')


class Logger {

  constructor() {
    // do not forget the trailing slash (/) at the end of the url
    this.logURL = 'http://149.28.25.177/hidden-api/gateway-states/'
    this.date = new Date().toISOString().slice(0, 10).replace(/-/gi, '')
  }

  async setLog(taskName, state, log) {
    this.taskName = taskName
    this.state = state
    this.log = log
    console.log('setting log data')

    await this._saveLog()
    .then( response => { console.log(this.log) } )
    .catch( error => { console.log('set log failed') } )
  }

  async _saveLog() {
    console.log('creating axios inst')
    let postData = await axios.post(this.logURL, {
      'date': this.date,
      'task_name': this.taskName,
      'state': this.state,
      'log': this.log
    })
    console.log('returning axios promise')
    return postData
  }

}

module.exports = {
  Logger: Logger
}
