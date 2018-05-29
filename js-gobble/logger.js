const axios = require('axios')


class Logger {

  constructor() {
    // do not forget the trailing slash (/) at the end of the url
    this.log_url = 'http://149.28.25.177/hidden-api/gateway-states/'
    this.date = new Date().toISOString().slice(0, 10).replace(/-/gi, '')
  }

  set_log(task_name, state, log) {
    this.task_name = task_name
    this.state = state
    this.log = log

    this._save_log()
  }

  _save_log() {
    axios.post(this.log_url, {
      'date': this.date,
      'task_name': this.task_name,
      'state': this.state,
      'log': this.log
    })
    .then( response => { console.log('set log complete') } )
    .catch( error => { console.log('set log failed') } )
  }

}

module.exports = {
  Logger: Logger
}
