function initMap() {

    var location = {lat: 45.229303, lng: 17.517473};
    var map = new google.maps.Map(document.getElementById("map"), 
    {
        zoom: 13,
        center: location
    });
    var marker = new google.maps.Marker({
        position: location,
        map: map
    });

}
