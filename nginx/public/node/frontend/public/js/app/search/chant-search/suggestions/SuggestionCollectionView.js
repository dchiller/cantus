import _ from 'underscore';
import $ from 'jquery';
import Marionette from 'marionette';

import SuggestionView from './SuggestionView';
import template from './suggestion-collection.template.html';

export default Marionette.CompositeView.extend({
    template: template,

    childView: SuggestionView,
    childViewContainer: "div",

    sort: false,

    ui: {
        'suggestion': 'div.list-group'
    },

    events: {
        'mousedown @ui.suggestion': 'suggestionClicked',
        'touchstart @ui.suggestion': 'suggestionClicked' // Touch support
    },

    initialize: function ()
    {
        _.bindAll(this, 'show', 'hide', 'keyDown');
        this.hide(); // Hide the suggestions initially
    },

    suggestionClicked: function (e)
    {
        // Triggers "setQuery" in the SearchInputView through the ChantSearchProvider
        var el = $(e.target).closest('a.list-group-item');

        this._setActive(el);
        this._searchActiveSuggestion();
    },

    _setActive: function (el)
    {
        this.$('.active').removeClass('active');
        el.addClass('active');
    },

    _searchActiveSuggestion: function ()
    {
        // Get the active suggestion
        var el = this.$('.active');
        // Add boolean operator 'AND' between all words, in order to match exactly the suggestion
        var text = el.text()
        if (text.startsWith('"')){
            text = text.slice(1,0);
        }
        if (text.endsWith('"')){
            text = text.slice(0,-1);
        }
        text = `"${text}"`
        this.trigger('click:suggestion', null, text);
        this.hide();
    },

    show: function()
    {
        this.$el.show();
    },

    hide: function ()
    {
        this.$el.hide();
    },

    keyDown: function (keyCode)
    {
        this.show(); // Make sure the suggestions are shown when typing

        var el;
        switch (keyCode)
        {
            // Enter key
            case 13:
                if (!this.$('.active').length){
                    // If there is no active suggestion, search for
                    // first suggestion.
                    el = this.$('a.list-group-item:first');
                    if (el.length)
                        this._setActive(el);
                    else {
                        break;
                    }
                }
                this._searchActiveSuggestion();
                break;

            // Up arrow
            case 38:
                el = this.$('.active').prev();
                if (el.length)
                    this._setActive(el);
                else
                    this._setActive(this.$('a.list-group-item:last'));
                break;

            // Down arrow
            case 40:
                el = this.$('.active').next();
                if (el.length)
                    this._setActive(el);
                else
                    this._setActive(this.$('a.list-group-item:first'));
                break;
        }
    }
});
