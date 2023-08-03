import Marionette from "marionette";
import Backbone from "backbone";
import $ from 'jquery';

import navitemtemplate from "./nav-item.template.html";

var manuscriptChannel = Backbone.Radio.channel('manuscript');

var NavItemModel = Backbone.Model.extend({});

var NavMenuCollection = Backbone.Collection.extend({
    model: NavItemModel
});

var folioNavOptions = [
    {navTitle:"Folio 2r", 
    imageLink:"http://169.254.175.5/iiif/2/Salzinnes-I_002r.tiff", 
    navDescription: "The Annunciation"},
    {navTitle:"Folio 33r", 
    imageLink:"http://169.254.175.5/iiif/2/Salzinnes-I_033r.tiff", 
    navDescription: "The Nativity"},
    {navTitle:"after Folio 45v", 
    imageLink:"http://169.254.175.5/iiif/2/Salzinnes-I_045_2.tiff", 
    navDescription: "The Adoration of the Magi"},
    { navTitle: "after Folio 50v", 
    imageLink:"http://169.254.175.5/iiif/2/Salzinnes-I_050_1.tiff", 
    navDescription: "The Baptism of Christ"},
    { navTitle: "after Folio 117v", 
    imageLink:"http://169.254.175.5/iiif/2/Salzinnes-I_117_2.tiff", 
    navDescription: "The Agony in the Garden of Gethsemane"},
    { navTitle: "after Folio 124v", 
    imageLink:"http://169.254.175.5/iiif/2/Salzinnes-I_126v.tiff", 
    navDescription: "The Resurrection"},
    { navTitle: "after Folio 124v", 
    imageLink:"http://169.254.175.5/iiif/2/Salzinnes-I_126v.tiff", 
    navDescription: "The Assembly of the Saints"},
    { navTitle: "after Folio 133v",
    imageLink:"http://169.254.175.5/iiif/2/Salzinnes-I_133_2.tiff", 
    navDescription: "Holy Kinship"},
    { navTitle: "Folio A24v", 
    imageLink:"http://169.254.175.5/iiif/2/Salzinnes-II_24v.tiff", 
    navDescription: "Saint Maurice"},
    { navTitle: "Folio A30r", 
    imageLink:"http://169.254.175.5/iiif/2/Salzinnes-II_30r.tiff", 
    navDescription: "Saint Hubert"},
    { navTitle: "Folio A36v", 
    imageLink:"http://169.254.175.5/iiif/2/Salzinnes-II_36v.tiff", 
    navDescription: "Saint Juliana"}
    ]


const NavItemView =  Marionette.ItemView.extend({
        template: navitemtemplate,
        ui :{
            highlightCard: '.highlight-card'
        },
        events: {
            'click @ui.highlightCard': '_goToImage'
        },
        _goToImage: function(){
            manuscriptChannel.request('set:imageURI', this.model.get('imageLink'), {replaceState:true});
            $('#salzinnesNavMenuModal').modal('hide');
        }
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