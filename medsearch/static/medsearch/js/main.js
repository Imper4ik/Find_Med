let map;

function initMap() {
    // Определяем параметры карты
    const mapOptions = {
        center: { lat: 52.2296756, lng: 21.0122287 },
        zoom: 14,
    };

    // Инициализируем карту
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
    console.log("Map initialized");

    // Проверяем, поддерживает ли браузер геолокацию
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            const userLocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };

            console.log("User location:", userLocation);

            // Добавляем маркер на карту для текущего местоположения
            const userLocationMarker = new google.maps.Marker({
                position: userLocation,
                map: map,
                title: 'Your Location'
            });

            // Центрируем карту на текущее местоположение
            map.setCenter(userLocation);
        }, function(error) {
            console.log("Error getting geolocation: " + error.message);
        });
    } else {
        console.log('Geolocation is not supported by this browser.');
    }
}
