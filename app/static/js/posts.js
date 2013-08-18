$(document).ready(function() {
    if (Modernizr.geolocation) {
    
    var map = L.mapbox.map('cookie-map', 'egdelwonk.map-e1ydkdp5', {
        attributionControl: false
    });

    var postSource   = $("#post-template").html();
    var posTemplate = Handlebars.compile(postSource);

    var cookiePin = L.icon({
        iconUrl: '/static/img/cookie-pin.png',
        iconSize:     [23, 23], // size of the icon
        iconAnchor:   [0, 0], // point of the icon which will correspond to marker's location
        shadowAnchor: [4, 62],  // the same for the shadow
        popupAnchor:  [12, 5] // point from which the popup should open relative to the iconAnchor
    });
    
    var markers = L.markerClusterGroup();

    navigator.geolocation.watchPosition(function(position) {
        $('div.nomap').hide();
        $('div.location-shared').show();
        
        $('#new-message-form input[name=long]').val(position.coords.longitude);
        $('#new-message-form input[name=lat]').val(position.coords.latitude);


        var radiusBounds = L.circle([position.coords.latitude, position.coords.longitude], 1069, {
            color: '#e4e6e8',
            fillColor: '#2e3846',
            fillOpacity: 0.3,
            weight: 1
        }).addTo(map);
    
        map.fitBounds(radiusBounds.getBounds());

        $.get('/posts/list/' + position.coords.latitude + '/' + position.coords.longitude, function(data){
            var posts = data.result;
            for (var i = 0; i < data.result.length; i++) {
                var marker = L.marker([data.result[i].lat, data.result[i].long], {icon: cookiePin});
                marker.bindPopup(data.result[i].secret);
                markers.addLayer(marker);
            };
            map.addLayer(markers);
            $('#posts tbody').html(posTemplate({results: posts}));
        });
        
    });
    } else {
        $('div.container div').hide();
        $('div#unsupported').show();
    }

    $('.show-new-message-form').on('click', function(e) {
        e.preventDefault();
        $('#new-message-form').toggle();
        $('#new-message-form input[name=secret]').focus();
    });

    $('#new-message-form form').on('submit', function(e){
        e.preventDefault();
        $.post($(this).attr('action'),$(this).serialize(), function(data){
            var posts = data.result;
            markers.clearLayers();
            for (var i = 0; i < data.result.length; i++) {
                var marker = L.marker([data.result[i].lat, data.result[i].long], {icon: cookiePin});
                marker.bindPopup(data.result[i].secret);
                markers.addLayer(marker);
            };
        
            $('#posts tbody').html(posTemplate({results: posts}));

            $('#new-message-form').toggle();
            $('#new-message-form input[name=secret]').val('');
        });
    })

});
