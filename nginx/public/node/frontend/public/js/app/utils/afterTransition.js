import _ from "underscore";
import $ from "jquery";

/**
 * Call the callback function after the transitions for the element have completed,
 * or after the given number of milliseconds have elapsed if it is not possible
 * to detect the transition end.
 *
 * @param {jQuery} jqElem
 * @param {number} fallbackMs
 * @param {function} callback
 * @param {Object} context
 */
export default function afterTransition(jqElem, fallbackMs, callback, ctx) {
    jqElem
        .one("transitionend", _.bind(callback, ctx));
}
