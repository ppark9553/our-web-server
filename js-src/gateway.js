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

// constants/URLs here
const actionsURL = 'http://149.28.25.177/hidden-api/gateway-actions/'
let gatewayLogsURL = 'http://149.28.25.177/hidden-api/gateway-states/?ordering=created&date={0}&task_name={1}'
const taskURL = 'http://149.28.25.177/hidden-api/task/?type='

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

let runTask = (taskName) => {
  let fullTaskURL = taskURL + taskName
  return axios.get(fullTaskURL)
}

let loadLogs = (taskName) => {
  let date = new Date().toISOString().slice(0, 10).replace(/-/gi, '')
  let reqURL = gatewayLogsURL.format(date, taskName)
  return axios.get(reqURL)
}

let createLogsListHTML = (dataList, runServerFilter) => {
  let taskName = ''
  var color = ''
  let logRowsHTML = ''
  for (let data of dataList.data.results) {
    taskName = data.task_name
    let runServer = data.log.split(':')[0]
    if ((runServer == runServerFilter) || (runServerFilter == 'all')) {
      switch (runServer) {
        case 'web':
          color = 'black'
          break
        case 'db':
          color = 'gray'
          break
        case 'cache':
          color = 'red'
          break
        case 'gateway':
          color = 'green'
          break
        case 'gobble':
          color = 'blue'
          break
        case 'js-gobble':
          color = 'purple'
          break
        case 'mined':
          color = 'brown'
          break
      }
      logRowsHTML = logRowsHTML + logRowHTML.format(data.created, color, data.log)
    } else {
      // pass
    }
  }
  return logAreaHTML.format(taskName, logRowsHTML)
}

let createLogsList = (logsListHTML) => {
  // get content-body section and switch to logsListHTML
  let contentBody = document.getElementsByClassName('content-body')[0]
  contentBody.innerHTML = logsListHTML
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
<div class="content-title">
  <strong>{0}</strong>
  <div class="enabled check-db-btn">
    Check DB
  </div>
</div>
<div class="task-tags">
  <div id="task-tag" class="all task-tag black" name="all">ALL</div>
  <div id="task-tag" class="task-tag black" name="web">web</div>
  <div id="task-tag" class="task-tag gray" name="db">db</div>
  <div id="task-tag" class="task-tag red" name="cache">cache</div>
  <div id="task-tag" class="task-tag green" name="gateway">gateway</div>
  <div id="task-tag" class="task-tag blue" name="gobble">gobble</div>
  <div id="task-tag" class="task-tag purple" name="js-gobble">js-gobble</div>
  <div id="task-tag" class="task-tag brown" name="mined">mined</div>
</div>
<div class="log-body">
  {1}
</div>
`

let logRowHTML = `
<div class="log-row">
  <div class="log-created">{0}</div>
  <div class="{1} log-content">{2}</div>
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

var applyTaskLogFilter = false // when loading logs for the first time, this should be false
document.addEventListener("click", e => {

    if (e.target.id == 'run') {
      let taskRowText = e.target.parentNode.parentNode.innerText
      let textList = taskRowText.split(/(\s+)/)
      let taskName = textList[0]
      updateLog(taskName + ' clicked, task running (check logs)')

      runTask(taskName)
      .then( reply => { console.log(reply) })
      .catch( error => { console.log(error) })
    }

    // only run this event when applyTaskLogFilter is false, meaning page is loading logs for the first time
    else if ((e.target.id == 'task-log') && (applyTaskLogFilter == false)) {
      let taskRowText = e.target.parentNode.parentNode.innerText
      let textList = taskRowText.split(/(\s+)/)
      let taskName = textList[0]
      updateLog(taskName + ' log check clicked')

      loadLogs(taskName)
      .then( reply => createLogsListHTML(reply, 'all') )
      .then( reply => createLogsList(reply) )

      applyTaskLogFilter = true // switch to true once first log load has been done
    }

    else if (e.target.id == 'task-tag') {
      let taskName = document.getElementsByClassName('content-title')[0]
      taskName = taskName.innerText.split(/(\s+)/)[0]

      let runServerFilter = e.target.getAttribute('name')
      updateLog('Filter: ' + runServerFilter + ' applied')
      loadLogs(taskName)
      .then( reply => createLogsListHTML(reply, runServerFilter) )
      .then( reply => createLogsList(reply) )
    }

    else if (e.target.id == 'back-btn') {
      updateLog('Returning back to tasks list...')
      loadTasks()
      .then( reply => createTasksListHTML(reply) )
      .then( reply => createTasksList(reply) )
      updateLog('Tasks list loaded')

      applyTaskLogFilter = false // this should be false, because user will have to set logs for the first time again
    }
})
