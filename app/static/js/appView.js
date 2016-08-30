var AppView = Backbone.View.extend({
  initialize: function($el, template, triePromise, input, suggestionsList, type) {
    this.setElement($el);
    this.$input = this.$el.find(input);
    this.$suggestions = this.$el.find(suggestionsList);
    this.tmpl = _.template(template);

    this.searchType = type;

    this.triePromise = triePromise;
  },
  render: function(suggestions) {
    var compiled = this.tmpl({suggestions: suggestions || []});
    this.$suggestions.html(compiled);
    return this;
  },

  /**
   * events:  keypress to get all keys,
   *          keydown to get backspace key (since keyDown seems to return incorrect keyCode)
   */
  events: {
    'keypress' : 'search',
    'keydown'  : 'wasSpecialKey'
  },

  menuItem: -1,

  // used for backspace, enter, and arrow up/down
  wasSpecialKey: function (key) {
    // backspace key
    if (key.keyCode === 8) {
      this.search();
    }

    // enter key
    if (key.keyCode === 13) {
      key.preventDefault();
      this.updateCourseInput();
      if (this.searchType === "course") {
        $("#add-class").trigger("click");
      } else if (this.searchType === "course-filter") {
          $("#filter-button").trigger("click");
      }
      this.menuItem = -1;
      this.search();
    }

    // in order: up, down
    if (key.keyCode === 38 ||
        key.keyCode === 40) {

      key.preventDefault();
      if (key.keyCode != 13) {
        this.removeHoverClass();
        switch (key.keyCode) {
          case 38:
            this.menuItem--;
            if (this.menuItem < 0) {
              this.menuItem = -1;
            }
            break;
          case 40:
            this.menuItem++;
            break;
        }
        this.addHoverClass();
      }
      this.updateCourseInput();
    }
  },

  addHoverClass: function() {
    var elt = $(".suggestions").children()[this.menuItem];
    $(elt).addClass("course-hover");
  },

  removeHoverClass: function() {
    if (this.menuItem >= 0) {
      var prev = $(".suggestions").children()[this.menuItem];
      $(prev).removeClass("course-hover");
    }
  },

  updateCourseInput: function() {
    if (this.menuItem >= 0) {
        var elt = $(".suggestions").children()[this.menuItem];
        var course = $(elt).text();
        if (this.searchType === "course") {
          $('input[name=course]').val(course);
        } else if (this.searchType === "course-filter") {
          $('input[name=course-filter]').val(course);
        }
      }
  },

  //used for all char keys
  search: function (key) {
    var that = this;
    var word = this.$input[0].value;
    if (key) {
      key = String.fromCharCode(key.keyCode);
      word += key;
    } else {
      word = word.substring(0,word.length - 1);
    }
    this.triePromise.then(function (trie) {
      that.render(trie.getSuggestions(word));
    });
  }
});

window.AppView = AppView;
