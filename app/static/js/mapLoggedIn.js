/*

map.js

This file contains all of the google map api required code

*/

// this user's name
var username;

// the map being displayed and updated
var map;

// the list of other user markers
var markers = [];

// grab the updates from this user's infobox and send them to the server
var getUpdates = function () {
    var curRoom = $("input[name=cur-room]").val();
    var curCourse = $("input[name=cur-course]").val();
    var curAssignment = $("input[name=cur-assignment]").val();

    var updates = {
      "course":curCourse,
      "room":curRoom,
      "assignment":curAssignment
    }

    $.get("http://localhost:8080/update", updates, function() {
      $("input[name=cur-room").val(curRoom);
      $("input[name=cur-course").val(curCourse);
      $("input[name=cur-assignment").val(curAssignment);

      $(".update-success-message").fadeIn(500).delay(1500).fadeOut(400);
    });
}

// TODO:  implement this thing
var joinUser = function () {
  alert("Coming soon!");
}

// given an array of other users (as JSON objects) create markers and infoboxes for them and add them to the map
var populateMap = function (usersArray) {

  for (var i = 0; i < usersArray.length; i++) {
    var thisUser = usersArray[i];
    var name = thisUser['firstname'] + " " + thisUser['lastname'];

    // skip this user such that his/her pin isn't dropped twice
    if (name === username) {
      continue;
    }

    var gender = thisUser['gender'];
    var bio = thisUser['bio'];

    var curCourse = thisUser['curCourse'] ? thisUser['curCourse'] : "unspecified";
    var curRoom = thisUser['curRoom'] ? thisUser['curRoom'] : "unspecified";
    var curAssignment = thisUser['curAssignment'] ? thisUser['curAssignment'] : "unspecified";

    var picture = "generic-user";
    if (gender === "M") {
      picture += "-male"
    } else if (gender === "F") {
      picture += "-female";
    }

    var location = thisUser['location'];
    var coords = location.split(", ");

    // remove the front parenthesis
    var lat = coords[0].substring(1,coords[0].length);

    // remove the back parenthesis
    var lon = coords[1].substring(0,coords[1].length - 1);
    var pos = new google.maps.LatLng(lat, lon);


    var userHTML =
        "<div class='userContent'>"+
          "<h1>" + name + "</h1>"+
          "<div>"+
            "<img border='0' width='200' src='./static/img/" + picture + ".png'>"+
            "<p><i>" + bio + "</i></p>" +
            "<p style='text-align:left'><b>Currently Working On:</b> <span style='float:right'>" + curCourse + "</span></p>"+
            "<p style='text-align:left'><b>Currently in Room:</b> <span style='float:right'>" + curRoom + "</span></p>"+
            "<p style='text-align:left'><b>Having Difficulty With:</b> <span style='float:right'>" + curAssignment + "</span></p>"+
            "<input class='join-button' type='button' onclick='joinUser()' value='Form Study Group!'>"+
          "</div>"+
        "</div>";
        
    var userMarker = new google.maps.Marker({
      position: pos,
      map: map,
      title: name
    });
    markers.push(userMarker);

    var userInfo = new google.maps.InfoWindow({
      map: map,
      position: pos,
      content: userHTML
    });

    makeInfoWindowEvent(map, userInfo, "", userMarker);
    
    userInfo.close();
  }
}

// remove all other user markers from the map and clear the list
var deleteOldMarkers = function() {
  console.log("here");
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(null);
  }
  markers = [];
}

// provided google maps api function:  if there is no geolocation data, message displayed on map
function handleNoGeolocation(errorFlag) {
  if (errorFlag) {
    var content = 'Error: The Geolocation service failed.';
  } else {
    var content = 'Error: Your browser doesn\'t support geolocation.';
  }
  var options = {
    map: map,
    position: new google.maps.LatLng(60, 105),
    content: content
  };

  var infowindow = new google.maps.InfoWindow(options);
  map.setCenter(options.position);
}

// bind user infobox to that user's marker
function makeInfoWindowEvent(map, infowindow, contentString, marker) {
  google.maps.event.addListener(marker, 'click', function() {
    infowindow.open(map, marker);
  });
}

$(document).ready(function() {

  // grab the other users from the HTML (these are the users that fit the filter query)
  var jsonstring = $('#hidden-json').text();
  var arr = jsonstring.split(";");

  var usersArray = [];

  for (var i = 0; i < arr.length - 1; i++) {
    usersArray.push(JSON.parse(arr[i]));
  }

  // initialize the map
  function initialize() {
    // center map on campus, zoom to see most the campus, and prevent default map functionalities (except zoom)
    var mapOptions = {
      center: { lat: 39.9538, lng: -75.5900},
      zoom: 16,
      disableDefaultUI: true
  	};

    // grab this user from the HTML (it appears as a hidden JSON object) and parse info
    var thisUser = JSON.parse($("div.hidden-user-json").text());

    username = thisUser["firstname"] + " " + thisUser["lastname"];
    var gender = thisUser["gender"];
    var picture = "generic-user";
    if (gender === "M") {
      picture += "-male"
    } else if (gender === "F") {
      picture += "-female";
    }

    var curCourse = thisUser['curCourse'] ? thisUser['curCourse'] : "";
    var curRoom = thisUser['curRoom'] ? thisUser['curRoom'] : "";
    var curAssignment = thisUser['curAssignment'] ? thisUser['curAssignment'] : "";

  	var contentString =
  		"<div id='content'>"+
  			"<h1 class='firstHeading'>" + username + "</h1>"+
  			"<div id='bodyContent'>"+
  				"<img border='0' width='200' src='./static/img/" + picture + ".png'>"+
          "<div class='update-success-message'>Updated Successfully!</div>" +
  				"<p style='text-align:right'><b>Currently Working On:</b> <input type='text' name='cur-course' value='" + curCourse + "'></p>"+
  				"<p style='text-align:right'><b>Currently in Room:</b> <input type='text' name='cur-room' value='" + curRoom + "'></p>"+
  				"<p style='text-align:right'><b>Having Difficulty With:</b> <input type='text' name='cur-assignment' value='" + curAssignment + "'></p>"+
  				"<input id='update-button' type='button' onclick='getUpdates()' value='Update'>"+
  			"</div>"+
  		"</div>";
  	        
  	map = new google.maps.Map(document.getElementById('map-canvas'),
  	            mapOptions);
    
    var infowindow;
    var marker;

    // Try HTML5 geolocation
    if(navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position) {
        var pos = new google.maps.LatLng(position.coords.latitude,
                                         position.coords.longitude);
        
        // set sign up form's hidden location field to this position
        $("#upLocation").val(pos);

        // set sign in form's hidden location field to this position
        $("#inLocation").val(pos);

        // create a marker at this position for this user
        marker = new google.maps.Marker({
          position: pos,
          map: map,
          title: username
        });

        // create an infobox for this user at this position
        infowindow = new google.maps.InfoWindow({
          map: map,
          position: pos,
          content: contentString
        });

        // bind infobox to the marker
        makeInfoWindowEvent(map, infowindow, "test", marker);

        // add other users to the map
        populateMap(usersArray);

        // center at this user
        map.setCenter(pos);
      }, function() {
        handleNoGeolocation(true);
      });
    } else {
      // Browser doesn't support Geolocation
      handleNoGeolocation(false);
    }     
  }

  google.maps.event.addDomListener(window, 'load', initialize);

});