var Trie = function (words) {
  this.data = {};
  _.each(words, function (word) {
    this.addWord(word,this.data);
  }.bind(this));
};

Trie.prototype.addWord = function (word, trieNode) {
  if (word === '') {
    trieNode['end'] = true;
    return;
  }

  word = word.toUpperCase();

  var first = word.split('',1).join();
  if (!(_.has(trieNode, first))) {
    trieNode[first] = {};
  }

  var newWord = (_.rest(word.split(''))).join('');
  var newNode = trieNode[first];
  this.addWord(newWord, newNode);
};

// getSuggestions helper function
Trie.prototype.getWords = function(letters, trieNode) {
  var that = this;

  // array to hold strings that are complete words
  var arr = [];

  // a switch that will flip off after the first child is read
  var first = true;

  // for each child of trieNode, push the word or get words from its children
  _.each(trieNode, function(val, key) {
    if (key === 'end') {
      arr.push(letters.join(''));
    } else {
      letters.push(key);
      var more = that.getWords(letters,trieNode[key]);
      letters.pop();
      arr = arr.concat(more);
    }
  });

  return arr;
}

// getSuggestions helper function
Trie.prototype.contains = function(letters, trieNode) {
  // the trieNode always contains the empty array
  if (letters.length === 0) {
    return true;
  }

  //get first letter
  var cur = letters[0];

  //if trieNode has that child, keep checking until letters is empty
  if (_.has(trieNode, cur)) {
    return this.contains(_.rest(letters), trieNode[cur]);
  } else {
    return false;
  }
}

Trie.prototype.getSuggestions = function(sub) {
  var that = this;
  sub = sub.toUpperCase();

  var arr = [];
  
  var letters = sub.split('');
  var trieNode = that.data;

  //if sub is empty or the trie does not contain sub, return the empty array
  if (sub === '' || !that.contains(letters, that.data)) {
    return arr;
  } else {
    //get to trieNode of last letter
    for (var i = 0; i < letters.length; i++) {
      trieNode = trieNode[letters[i]];
    }
    arr = that.getWords(letters, trieNode);
    return arr;
  }
};

window.Trie = Trie;