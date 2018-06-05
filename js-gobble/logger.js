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
    this.log = 'js-gobble: ' + log

    await this._saveLog()
    .then( response => { console.log(this.log) } )
    .catch( error => { console.log('set log failed') } )
  }

  async _saveLog() {
    let postData = await axios.post(this.logURL, {
      'date': this.date,
      'task_name': this.taskName,
      'state': this.state,
      'log': this.log
    })
    return postData
  }

}

module.exports = {
  Logger: Logger
}
