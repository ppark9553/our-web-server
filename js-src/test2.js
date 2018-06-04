class TestClass {
  constructor() {
    this.greetings = 'this is a test greeting from TestClass'
  }

  testGreeting() {
    console.log(this.greetings)
    return true
  }
}

module.exports = {
  TestClass: TestClass
}
