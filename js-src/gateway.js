import io from 'socket.io-client'

// define functions here
let updateLog = log => {
  let logEl = document.getElementById('log')
  logEl.innerText = log
}

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
    }
})
