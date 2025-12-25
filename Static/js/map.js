function initMap() {
    let defaultLocation = { lat: 12.9716, lng: 77.5946 }; 

    const map = new google.maps.Map(document.getElementById("map"), {
        center: defaultLocation,
        zoom: 13,
    });

    const marker = new google.maps.Marker({
        map: map,
        draggable: true,
        position: defaultLocation,
    });

    const input = document.getElementById("search");
    const searchBox = new google.maps.places.SearchBox(input);

    map.addListener("bounds_changed", () => {
        searchBox.setBounds(map.getBounds());
    });

    searchBox.addListener("places_changed", () => {
        const places = searchBox.getPlaces();

        if (places.length === 0) return;

        marker.setMap(null); 
        const bounds = new google.maps.LatLngBounds();
        places.forEach((place) => {
            if (!place.geometry || !place.geometry.location) {
                console.log("Returned place contains no geometry");
                return;
            }

            marker.setPosition(place.geometry.location);
            marker.setMap(map);

            if (place.geometry.viewport) {
                bounds.union(place.geometry.viewport);
            } else {
                bounds.extend(place.geometry.location);
            }
        });
        map.fitBounds(bounds);
    });

    function centerToCurrentLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const userLocation = {
                        lat: position.coords.latitude,
                        lng: position.coords.longitude,
                    };

                    map.setCenter(userLocation);
                    marker.setPosition(userLocation);
                    marker.setMap(map);
                },
                () => {
                    console.warn("Geolocation permission denied or failed.");
                    alert("Unable to access your location.");
                }
            );
        } else {
            console.warn("Geolocation is not supported by this browser.");
            alert("Geolocation is not supported by your browser.");
        }
    }


    const locButton = document.querySelector(".loc");
    locButton.addEventListener("click", centerToCurrentLocation);

    centerToCurrentLocation();
}

window.onload = initMap;
