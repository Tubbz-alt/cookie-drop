$(document).ready(function() {

    if (Modernizr.geolocation) {
     navigator.geolocation.getCurrentPosition(function(position){
        $('div.nomap').hide();
        $('div#location-shared').show();
        var map = L.mapbox.map('cookie-map', 'egdelwonk.map-e1ydkdp5', {
            center: [position.coords.latitude, position.coords.longitude],
            zoom: 18,
            attributionControl: false
        });
     });
    } else {
        $('div.container div').hide();
        $('div#unsupported').show();
    }
});
