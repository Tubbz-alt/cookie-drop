$(document).ready(function() {
    if (Modernizr.geolocation) {
     navigator.geolocation.getCurrentPosition(function(position){
        $('div.nomap').hide();
        $('div.location-shared').show();
        
        var map = L.mapbox.map('cookie-map', 'egdelwonk.map-e1ydkdp5', {
            attributionControl: false
        });


        $('#new-message-form input[name=long]').val(position.coords.longitude);
        $('#new-message-form input[name=lat]').val(position.coords.latitude);


        var radiusBounds = L.circle([position.coords.latitude, position.coords.longitude], 1069, {
            color: '#e4e6e8',
            fillColor: '#2e3846',
            fillOpacity: 0.3,
            weight: 1
        }).addTo(map);
    
        map.fitBounds(radiusBounds.getBounds());

        var userPin = L.icon({
            iconUrl: '/static/img/user-pin.png',
            iconSize:     [33, 62],
            iconAnchor:   [16, 62]
        });

        var cookiePin = L.icon({
            iconUrl: '/static/img/cookie-pin.png',
            iconSize:     [23, 23], // size of the icon
            iconAnchor:   [-10, 84], // point of the icon which will correspond to marker's location
            shadowAnchor: [4, 62],  // the same for the shadow
            popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
        });

        L.marker([position.coords.latitude, position.coords.longitude], {icon: userPin}).addTo(map);

        $.get('/posts/list/' + position.coords.latitude + '/' + position.coords.longitude, function(data){
            for (var i = 0; i < data.result.length; i++) {
                L.marker([data.result[i].lat, data.result[i].long], {icon: cookiePin}).addTo(map);
            };
        });

     });

    } else {
        $('div.container div').hide();
        $('div#unsupported').show();
    }
});
$('.show-new-message-form').on('click', function(e) {
    e.preventDefault();
    $('#new-message-form').toggle();
    $('#new-message-form input[name=secret]').focus();
});
