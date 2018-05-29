const axios = require('axios')

// import with require from other node modules and set/save log
exports.set_log = (task_name, state, log) => {
  let gateway_url = 'http://149.28.25.177/hidden-api/gateway-states/'
  let date = new Date().toISOString().slice(0, 10).replace(/-/gi, '')
  axios.post(gateway_url, {
    'date': date,
    'task_name': task_name,
    'state': state,
    'log': log
  })
  .then( response => { console.log('set log complete') } )
  .catch( error => { console.log('set log failed') } )
}
