// $(document).ready(function() {
//
// })

var dropdownStatus = 'closed'

$(document).on('click', '#port-dropdown-menu', function() {
  if (dropdownStatus == 'closed') {
    $("#port-dropdown-section").removeClass('inactive')
    $("#port-dropdown-section").addClass('active')
    dropdownStatus = 'opened'
  } else if (dropdownStatus == 'opened') {
    $("#port-dropdown-section").removeClass('active')
    $("#port-dropdown-section").addClass('inactive')
    dropdownStatus = 'closed'
  }
})

// closing dropdown menu click when outside of the element
$(document).mouseup(function(e) {
  var container = $('.port-choices')

  // if the target of the click isn't the container nor a descendant of the container
  if (!container.is(e.target) && container.has(e.target).length === 0) {
    $("#port-dropdown-section").removeClass('active')
    $("#port-dropdown-section").addClass('inactive')
    dropdownStatus = 'closed'
  }
})
