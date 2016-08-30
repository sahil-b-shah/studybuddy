/**
* course.js
*
*/
$(document).ready(function () {

	// temp database of classes
	var classData = multiGet('http://cis197.herokuapp.com/departmentURLs.json',
                            'http://cis197.herokuapp.com/');
    var triePromise = trieFromDataPromise(classData);
  	var courseSearch = new AppView($('#course-search'), $('#item-template').html(), triePromise, '#course-input', '#course-suggestions-list', 'course');
  	var filterSearch = new AppView($('#course-filter-search'), $('#item-template').html(), triePromise,
  		'#course-filter-input', '#course-filter-suggestions-list', 'course-filter');

	var classes = "";
	var courseNum = 1;


	$('#add-class').on('click', function() {
		var c = $('input[name=course]').val();

		$('#courseKart').append("<li class='course-kart-item' id='course" + courseNum + "'>" + c +
			"<div class='remove-course-from-kart' id='remove-course-" + courseNum + "'>x</div></li>");

		var cur = courseNum;

		$('#remove-course-' + cur).on('click', function() {
			$('#course' + cur).remove();
		});

		courseNum++;

		classes += c + ";";

		$('#courses').val(classes);

		$('#course-input').val("");
	});

});
