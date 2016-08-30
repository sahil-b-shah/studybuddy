/**
 * Given a URL and a base URL, performs the following steps:
 * 1. GETs an array of JSON file names from the URL
 * 2. Adds each of these filenames to the base URL to obtain a list of URLs
 * 3. GETs each of these filenames (the data will be an array of strings)
 * 4. Returns an array that contains the combined output of each of the
 *     JSON files as a string list.
 * @param {string} url The original URL to GET
 * @param {string} baseUrl The base URL for the data JSON documents.
 * @returns {Promise<string[]>}
 */
var multiGet = function (url, baseUrl) {
	var ret = [];
	var ret = ajaxGet(url).then(function (data) {
		var arr = [];
		_.each(data, function(elt) {
			var newURL = baseUrl + elt;
			arr.push(ajaxGet(newURL));
		});
		return arr;
	});
	
	return Promise.all(ret);
};

/**
 * Returns a promise for a trie given a promise that resolves with a string array as data.
 * @param {Promise<string[]>} dataPromise A promise for the string array that will be used for the trie.
 * @returns {Promise<Trie>}
 */
var trieFromDataPromise = function (dataPromise) {
  return new Promise(function (resolve) {
  	dataPromise.then(function (data) {
  		var arr = [];
  		_.each(data, function (elt) {
  			_.each(elt, function (e) {
  				arr.push(e);
  			});
  		});
  		resolve(new Trie(arr));
  	});
  });
}

window.trieFromDataPromise = trieFromDataPromise;
