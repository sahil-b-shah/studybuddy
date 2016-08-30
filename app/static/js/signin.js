/*

signin.js

*/

$(document).ready(function() {

	$('#signup-button').on('click', function() {
		$('#signup-form').toggle(500);
	});

	$('#login-button').on('click', function() {
		$('#login-form').toggle(500);
	});

});