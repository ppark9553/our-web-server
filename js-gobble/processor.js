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
      }
    }

    return datesData
  }

  async processMassSD(date) {
    let jsonDate = date
    // sending JSON data to cache doesn't seem to work
    // add all needed data to string var and send full data as list
    let sdData = ['mass_sd']
    for (let obj of this.data.Data) {
      for (let json of obj) {
        console.log(json)
        let jsonMashed = ''
        let infoMashed = `{0};{1};{2};`.format(jsonDate, json['GICODE'], json['GINAME'])
        let forMashed = `{0};{1};{2};`.format(json['FORGN_B'], json['FORGN_S'], json['FORGN_N'])
        let indMashed = `{0};{1};{2};`.format(json['PRIVATE_B'], json['PRIVATE_S'], json['PRIVATE_N'])
        let insMashed = `{0};{1};{2};`.format(json['INST_B'], json['INST_S'], json['INST_N'])
        let trustMashed = `{0};{1};{2};`.format(json['TRUST_B'], json['TRUST_S'], json['TRUST_N'])
        let pensionMashed = `{0};{1};{2};`.format(json['PENSION_B'], json['PENSION_S'], json['PENSION_N'])
        let etcInstMashed = `{0};{1};{2}`.format(json['ETC_INST_B'], json['ETC_INST_S'], json['ETC_INST_N'])
        jsonMashed = jsonMashed + infoMashed + forMashed + indMashed + insMashed + trustMashed + pensionMashed + etcInstMashed
        sdData.push(jsonMashed)
        break
      }
      break
    }

    return sdData
  }

}

module.exports = {
  Processor: Processor
}
