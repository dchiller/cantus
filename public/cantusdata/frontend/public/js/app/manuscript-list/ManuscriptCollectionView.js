import Marionette from "marionette";
import ManuscriptItemView from "./ManuscriptItemView";

export default Marionette.CollectionView.extend({
    tagName: 'tbody',

    childView: ManuscriptItemView,
    emptyView: Marionette.ItemView.extend({
        tagName: 'tr',
        template: '#manuscript-collection-empty-template'
    })
});