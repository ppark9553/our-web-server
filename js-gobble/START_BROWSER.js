const Fnguide = require('./fnguide.js')

const main = async () => {
  let fn = new Fnguide.Puppet('')
  await fn.startBrowser(false, 100)
  .then( response => { console.log(response) })
  .catch( error => { console.log(error) })
}

main()
