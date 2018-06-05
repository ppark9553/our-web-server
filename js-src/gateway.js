import io from 'socket.io-client'

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

// define functions here
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
  <div class="task-name">{0}L</div>
  <div class="task-actions">
    <div id="run" class="task-btn">RUN</div>
    <div id="task-log" class="task-btn">LOG</div>
  </div>
</div>
`

let logAreaHTML = `
<div class="log-area">
  <div class="content-title"><strong>{0}</strong></div>
  <div class="log-body">
    {1}
  </div>
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
})

document.addEventListener("click", e => {
    if (e.target.id == 'run') {
      let taskRowText = e.target.parentNode.parentNode.innerText
      let textList = taskRowText.split(/(\s+)/)
      let taskName = textList[0]
      updateLog(taskName + ' clicked')
    } else if (e.target.id == 'task-log') {
      let taskRowText = e.target.parentNode.parentNode.innerText
      let textList = taskRowText.split(/(\s+)/)
      let taskName = textList[0]
      updateLog(taskName + ' log check clicked')

      // get content-body section and switch to logAreaHTML
    }
})