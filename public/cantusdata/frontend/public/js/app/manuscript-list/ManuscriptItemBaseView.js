import Marionette from "marionette";

/**
 * Shared base class for presenting manuscript table entries, extended
 * further for current and future manuscripts
 */
export default Marionette.ItemView.extend({
    template: '#manuscript-item-template',
    tagName: 'tr',

    ui: {
        tooltips: '[data-toggle=tooltip]'
    },

    onRender: function ()
    {
        // Initialize tooltips
        this.ui.tooltips.tooltip();
    }
});