import io from 'socket.io-client'
import axios from 'axios'

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

// constants here
const actionsURL = 'http://149.28.25.177/hidden-api/gateway-actions/'

///////////////////////////
// define functions here //
///////////////////////////
let loadTasks = () => {
  // this function is ran when website is first loaded
  // sends a request to gateway server for gateway actiosn list
  return axios.get(actionsURL)
}

let createTasksListHTML = (dataList) => {
  let taskRowsHTML = ''
  for (let data of dataList.data.results) {
    taskRowsHTML = taskRowsHTML + taskRowHTML.format(data.type)
  }
  return taskListHTML.format(taskRowsHTML)
}

let createTasksList = (tasksListHTML) => {
  // get content-body section and switch to tasksListHTML
  let contentBody = document.getElementsByClassName('content-body')[0]
  contentBody.innerHTML = tasksListHTML
}

let loadLogs = (taskName) => {

}


let updateLog = log => {
  let logEl = document.getElementById('log')
  logEl.innerText = log
}

// plugin task rows
let taskListHTML = `
<div class="content-title"><strong>Tasks List</strong></div>
<div class="task-body">{0}</div>
</div>
`

// plugin task name
let taskRowHTML = `
<div class="task-row">
  <div class="task-name">{0}</div>
  <div class="task-actions">
    <div id="run" class="task-btn">RUN</div>
    <div id="task-log" class="task-btn">LOG</div>
  </div>
</div>
`

let logAreaHTML = `
<div class="back-btn-section">
  <div id="back-btn" class="back-btn">
    << BACK
  </div>
</div>
<div class="content-title"><strong>{0}</strong></div>
<div class="task-tags">
  <div class="task-tag black">web</div>
  <div class="task-tag gray">db</div>
  <div class="task-tag red">cache</div>
  <div class="task-tag green">gateway</div>
  <div class="task-tag blue">gobble</div>
  <div class="task-tag purple">js-gobble</div>
  <div class="task-tag brown">mined</div>
</div>
<div class="log-body">
  {1}
</div>
`

// ip address should be that of gateway server
const socket = io('http://149.28.25.177:3000')

socket.on('connected', function(data) {
  if (data.connected == true) {
    updateLog('buzzz webpage ready to load with changes in DB')
  }
  socket.emit('ready for data', {})
})

socket.on('update', function(data) {
  updateLog(data.message.payload)
})

///// document related event listeners here /////
document.addEventListener("DOMContentLoaded", event => {
  updateLog('webpage fully loaded, gateway page starting')

  loadTasks()
  .then( reply => createTasksListHTML(reply) )
  .then( reply => createTasksList(reply) )
})

document.addEventListener("click", e => {

    if (e.target.id == 'run') {
      let taskRowText = e.target.parentNode.parentNode.innerText
      let textList = taskRowText.split(/(\s+)/)
      let taskName = textList[0]
      updateLog(taskName + ' clicked')
    }

    else if (e.target.id == 'task-log') {
      let taskRowText = e.target.parentNode.parentNode.innerText
      let textList = taskRowText.split(/(\s+)/)
      let taskName = textList[0]
      updateLog(taskName + ' log check clicked')

      // get content-body section and switch to logAreaHTML
      let contentBody = document.getElementsByClassName('content-body')[0]
      contentBody.innerHTML = logAreaHTML.format('logging logging')
    }

    else if (e.target.id == 'back-btn') {
      updateLog('Returning back to tasks list...')
      loadTasks()
      .then( reply => createTasksListHTML(reply) )
      .then( reply => createTasksList(reply) )
      updateLog('Tasks list loaded')
    }
})
