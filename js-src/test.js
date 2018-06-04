import { TestClass } from './test2.js'

import axios from 'axios' // works

// TEST INITIAL: test function call on load
document.addEventListener("DOMContentLoaded", event => {
  console.log('TEST INITIAL: function call on load works')
})

// TEST 1: test es6 transpile
let testTranspile = () => {
  console.log('es6 transpile success')
}

// TEST 2: test es6 constants and variable formatting
const constVar = 'a es6 constant variable'

let printConstVar = () => {
  console.log(`${constVar}`)
}

// TEST 3: can access class from other js files
let testClass = new TestClass()
testClass.testGreeting()

// TEST 4: js can access DOM elements from within js files
// also test whether async functions work as well
let asyncPrint = async (text) => {
  console.log(text)
}

let bodyText = document.getElementsByClassName("test-body")[0].innerText
asyncPrint(bodyText)

// TEST 5: test axios import and API fetching
let testURL = 'http://149.28.25.177/hidden-api/gateway-states/'

let getURL = async (testURL) => {
  console.log('creating axios inst')
  let getData = await axios.get(testURL)
  console.log('returning axios promise')
  return getData
}

let getData = async () => {
  await getURL(testURL, { crossdomain: true })
  .then( response => { console.log(response) })
  .catch( error => { console.log(error) })
}

document.addEventListener("click", e => {
    if (e.target.id == "get-btn") {
        getData()
    }
})
