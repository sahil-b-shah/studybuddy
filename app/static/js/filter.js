/*

filter.js

*/

$(document).ready(function() {
	$('#filter-button').on("click", function() {
		// get the filter value and create a JSON object with it
		var course = $("input[name=course-filter]").val();

		var filterOpt = {
			"course":course,
		}

		// send a get request to the server's '/filter' route
		$.get("http://localhost:8080/filter", filterOpt, function(data) {
			// on success, find the result JSON in the data
			var startIndex = data.indexOf("JSONbegin") + 64; // +64 because there are ALWAYS 64 characters until the beginning of the object in the HTML
			var endIndex = data.indexOf("JSONend") - 33; // -33 becuase there are ALWAYS 33 characters after the end of the object in the HTML

			// regex to fix quotes
			var re = new RegExp("&#34;", "g");

			// grab the string, fix the quotes, and split the string by semicolons into JSON objects 
			var jsonString = data.substring(startIndex, endIndex).replace(re, '"');
			var arr = jsonString.split(";");
			var usersArray = [];

			for (var i = 0; i < arr.length - 1; i++) {
				usersArray.push(JSON.parse(arr[i]));
			}

			// functions in mapLoggedIn.js
			deleteOldMarkers();
			populateMap(usersArray);

		});
	});
});