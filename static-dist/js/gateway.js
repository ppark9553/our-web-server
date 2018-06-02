// ajax call functions for gateway page

function webpageStarting() {
  console.log('buzzz gateway page starting')
}

function getRealTimeLog(id) {
  $.ajax({
    method: "POST",
    url: '/login/',
    data: {
        'email': email,
        'password': passwd
    },
    success: function(data){
      if (data == 200) {
        location.href = '/marketsignal'
      } else if (data == 400) {
        var msg = '아이디/비밀번호를 다시 확인해주세요'
        $('#msg-area').text(msg)
        $('#login_email').val('')
        $('#login_password').val('')
        $('#login_email').focus()
      }

    },
    error: function(data){
      console.log(data.status)
    }
  })
}

// $.ajax({
//   method: "POST",
//   url: '/login/',
//   data: {
//       'email': email,
//       'password': passwd
//   },
//   success: function(data){
//     if (data == 200) {
//       location.href = '/marketsignal'
//     } else if (data == 400) {
//       var msg = '아이디/비밀번호를 다시 확인해주세요'
//       $('#msg-area').text(msg)
//       $('#login_email').val('')
//       $('#login_password').val('')
//       $('#login_email').focus()
//     }
//
//   },
//   error: function(data){
//     console.log(data.status)
//   }
// })
