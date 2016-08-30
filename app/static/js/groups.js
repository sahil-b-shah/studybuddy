/*

groups.js

*/

$(document).ready(function() {
	var jsonstring = $('#hidden-group-json').text();
	var arr = jsonstring.split(";");

	var groupsArray = [];

	for (var i = 0; i < arr.length - 1; i++) {
		groupsArray.push(JSON.parse(arr[i]));
	}

	for (var i = 0; i < arr.length; i++) {
		var thisGroup = groupsArray[i];

		var name = thisGroup["group_name"];
		var id = thisGroup["group_id"];

		$("#group-list").append("<li class='group-list-item' id='group" + id + "'>" + name + 
			"<div class='join-group-from-list' id='join-group-" + id + "'>Join</div></li>");

		$("#join-group-" + id).on("click", function() {
			$.get("http://localhost:8080/group/join/" + id);
		});
	}
});