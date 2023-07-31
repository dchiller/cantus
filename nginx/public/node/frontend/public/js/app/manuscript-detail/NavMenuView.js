import Marionette from "marionette";
import Backbone from "backbone";

import navitemtemplate from "./nav-item.template.html";

var NavItemModel = Backbone.Model.extend({});

var NavMenuCollection = Backbone.Collection.extend({
    model: NavItemModel
});

var folioNavOptions = [
    {navTitle:"Folio 2r", 
    imageLink:"http://salzinnes-antiphonal/iiif/2/Salzinnes-I_002r.tiff/full/150,/0/default.jpg", 
    navDescription: "The Annunciation"},
    {navTitle:"Folio 33r", 
    imageLink:"http://salzinnes-antiphonal/iiif/2/Salzinnes-I_033r.tiff/full/150,/0/default.jpg", 
    navDescription: "The Nativity"},
    {navTitle:"after Folio 45v", 
    imageLink:"http://salzinnes-antiphonal/iiif/2/Salzinnes-I_045_2.tiff/full/150,/0/default.jpg", 
    navDescription: "The Adoration of the Magi"},
    { navTitle: "after Folio 50v", 
    imageLink:"http://salzinnes-antiphonal/iiif/2/Salzinnes-I_050_1.tiff/full/150,/0/default.jpg", 
    navDescription: "The Baptism of Christ"},
    { navTitle: "after Folio 117v", 
    imageLink:"http://salzinnes-antiphonal/iiif/2/Salzinnes-I_117_2.tiff/full/150,/0/default.jpg", 
    navDescription: "The Agony in the Garden of Gethsemane"},
    { navTitle: "after Folio 124v", 
    imageLink:"http://salzinnes-antiphonal/iiif/2/Salzinnes-I_126v.tiff/full/150,/0/default.jpg", 
    navDescription: "The Resurrection"},
    { navTitle: "after Folio 124v", 
    imageLink:"http://salzinnes-antiphonal/iiif/2/Salzinnes-I_126v.tiff/full/150,/0/default.jpg", 
    navDescription: "The Assembly of the Saints"},
    { navTitle: "after Folio 133v",
    imageLink:"http://salzinnes-antiphonal/iiif/2/Salzinnes-I_133_2.tiff/full/150,/0/default.jpg", 
    navDescription: "Holy Kinship"},
    { navTitle: "Folio A24v", 
    imageLink:"http://salzinnes-antiphonal/iiif/2/Salzinnes-II_24v.tiff/full/150,/0/default.jpg", 
    navDescription: "Saint Maurice"},
    { navTitle: "Folio A30r", 
    imageLink:"http://salzinnes-antiphonal/iiif/2/Salzinnes-II_30r.tiff/full/150,/0/default.jpg", 
    navDescription: "Saint Hubert"},
    { navTitle: "Folio A36v", 
    imageLink:"http://salzinnes-antiphonal/iiif/2/Salzinnes-II_36v.tiff/full/150,/0/default.jpg", 
    navDescription: "Saint Juliana"}
    ]


const NavItemView =  Marionette.ItemView.extend({
        template: navitemtemplate
    });

const NavMenuView = Marionette.CollectionView.extend({
    childView: NavItemView,
    tagName: 'div',
    className: 'highlight-collection',
    id: 'salzinnes-highlight-folios'
});

const testNavMenuCollection = new NavMenuCollection();
testNavMenuCollection.set(folioNavOptions);


export {NavMenuView, testNavMenuCollection}