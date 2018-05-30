class Processor {

  constructor(data) {
    this.data = data
  }

  async processMassDate() {
    let datesData = ['mass_date']

    for (let obj of this.data.Data) {
      for (let jsonData of obj) {
        let dateData = jsonData.TRD_DT.replace(/\./gi, '').trim()
        datesData.push(dateData)
        console.log(dateData + ' data pushed to list')
      }
    }

    return datesData
  }

}

module.exports = {
  Processor: Processor
}
