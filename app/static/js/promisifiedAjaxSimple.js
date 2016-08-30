/**
 * Returns a promise representing the value of a GET request to a URL.
 * @param {string} url The URL for the get requst.
 * @returns {Promise<object>}
 */
var ajaxGet = function (url) {
	return $.get(url, function (data) { return data; });
};

/**
 * Returns a promise for a trie given a remote URL that points to a JSON string array.
 * @param {string} url The URL for the data.
 * @returns {Promise<Trie>}
 */
 var trieFromURL = function (url) {
 	return new Promise(function(resolve) {
 		ajaxGet(url).then(function (data) {
 			resolve(new Trie(data));
 		});

 	});
 }

window.trieFromURL = trieFromURL;