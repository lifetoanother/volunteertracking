$(document).ready(function() {
	$("#submit-hours").on("click", function(e) {
		    e.preventDefault();
		    var jsondata = { "hours" : document.getElementById("HoursArea").value, "description" : document.getElementById("DescriptionArea").value }
		    $.ajax({type: "POST",
			            url: "/api/hours/month",
			    	    data: JSON.stringify(jsondata),
			    	    datatype: "json",
			            contentType: "application/json",
			        }).then(res => {
					console.log(res);
				});
	});
});
