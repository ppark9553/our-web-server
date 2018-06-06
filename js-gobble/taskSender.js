const Logger = require('./logger.js')
const CONFIG = require('./config.js')

const axios = require('axios')

const IP = CONFIG.ip.gateway


class TaskSender {

  constructor(taskName) {
    this.logger = new Logger.Logger()

    this.gatewayIP = IP
    this.taskURL = 'http://' + IP + '/hidden-api/task/?type='

    this.currentTask = taskName
  }

  async sendTask(nextTask) {
    taskURL = this.taskURL + nextTask
    await this._getTask(taskURL)
    .then( response => {
      if (response.data.status == 'DONE') {
        this.logger.setLog(this.currentTask, 'P', 'new task sent: ' + nextTask)
      } else if (response.data.staus == 'FAIL') {
        this.logger.setLog(this.currentTask, 'F', 'failed to send new task: ' + nextTask)
      } else if (response.data.status == ('NO ACTION: ' + nextTask)) {
        this.logger.setLog(this.currentTask, 'F', 'no action called: ' + nextTask)
      }
    })
    .catch( error => {
      this.logger.setLog(this.currentTask, 'F', 'js-gobble error')
    })
  }

  async _getTask(taskURL) {
    // named getData because sending request as GET request
    let getData = await axios.get(taskURL)
    return getData
  }

}

module.exports = {
  TaskSender: TaskSender
}
