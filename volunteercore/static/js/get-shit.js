/* eslint-env jquery */

$(document).ready(function () {
  $.ajax({
    url: '/api/hours/total',
    xhrFields: { withCredentials: true }
  }).then(function (data) {
    $('.hours-total').append(data.total_hours)
  })
})

$(document).ready(function () {
  $.ajax({
    url: '/api/hours/month',
    xhrFields: { withCredentials: true }
  }).then(function (data) {
    $('.hours-month').append(data.month_hours)
  })
})

$(document).ready(function () {
  $('#dataTable').DataTable({
    ajax: '/api/opportunities',
    columns: [
      { data: 'name', render: $.fn.dataTable.render.text() },
      { data: 'description', render: $.fn.dataTable.render.text() }
    ]
  })
})
