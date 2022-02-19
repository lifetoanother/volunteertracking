$(document).ready(function() {
    $.ajax({
        url: "/api/hours/total",
	xhrFields: { withCredentials:true }
    }).then(function(data) {
       $('.hours-total').append(data.total_hours);
    });
});

$(document).ready(function() {
    $.ajax({
        url: "/api/hours/month",
	xhrFields: { withCredentials:true }
    }).then(function(data) {
       $('.hours-month').append(data.month_hours);
    });
});

$(document).ready(function() {
    var table = $('#dataTables').DataTable( {
	"columns": [
		{ "data": "name" },
		{ "data": "description" },
		{ "data": "shift_hours" },
		{ "data": "volunteers_needed" }
	]
    });
    for ( var i = 0; i < 10; i++) {
	$.getJSON({
		url: "/api/opportunities",
		dataType: 'json',
		success: function (json) {
			table.rows.add(json.items).draw();
		}
	});
    }
} );
