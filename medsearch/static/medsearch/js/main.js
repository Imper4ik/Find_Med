let map;
let userLocationMarker;

function initMap() {
    const mapOptions = {
        center: { lat: 52.229675, lng: 21.012230 },
        zoom: 12,
    };

    map = new google.maps.Map(document.getElementById('map'), mapOptions);

    // Если поддержка геолокации есть
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const userLat = position.coords.latitude;
                const userLng = position.coords.longitude;

                const userLocation = new google.maps.LatLng(userLat, userLng);

                if (userLocationMarker) {
                    userLocationMarker.setMap(null); // Удаляем старый маркер
                }

                userLocationMarker = new google.maps.Marker({
                    position: userLocation,
                    map: map,
                    title: 'You are here',
                });

                map.setCenter(userLocation);
                map.setZoom(14);

                // Кнопка для расчета расстояния
                const findDistanceButton = document.getElementById('findDistanceBtn');
                findDistanceButton.addEventListener('click', function() {
                    calculateDistance(userLocation);
                });
            },
            () => {
                alert('Unable to retrieve your location');
            }
        );
    } else {
        alert('Geolocation is not supported by this browser');
    }
}

function calculateDistance(userLocation) {
    const service = new google.maps.DirectionsService();  // Используем DirectionsService

    const request = {
        origin: userLocation,  // Ваше местоположение
        destination: { lat: 52.285314, lng: 21.014551 },  // Координаты больницы (Mazovian "Bródnowski" Hospital)
        travelMode: google.maps.TravelMode.DRIVING
    };

    service.route(request, (result, status) => {
        if (status === google.maps.DirectionsStatus.OK) {  // Проверка статуса
            const distance = result.routes[0].legs[0].distance.text;
            console.log('Distance to hospital:', distance);
            alert('Distance to hospital: ' + distance);  // Покажем результат пользователю
        } else {
            console.error('Error calculating route:', status);
            alert('Error calculating route: ' + status);
        }
    });
}

// Загружаем Google Maps API, передавая ключ из контекста
function loadScript(src, callback) {
    const script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = src;
    script.onload = callback;
    document.body.appendChild(script);
}

// Подключаем Google Maps API с переданным ключом
loadScript("https://maps.googleapis.com/maps/api/js?key={{ google_api_key }}&libraries=places&callback=initMap", initMap);
