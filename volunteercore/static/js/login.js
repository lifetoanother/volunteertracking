$(document).ready(function() {
	$("#login-button").on("click", function(e) {
		    e.preventDefault();
		    const Authorization = 'Basic ' + window.btoa(document.getElementById("InputUsername").value + ':' + document.getElementById("InputPassword").value);

		    $.ajax({type: "POST",
			            url: "/api/auth/login",
			    	    headers: { 'Authorization' : Authorization },
			        }).then(res => {
					if (res.status == "user logged in") {
						location.href = "/index.html";
					}
					else {
						//TODO some code to tell the user that the login failed
					}
				});
	});
});
