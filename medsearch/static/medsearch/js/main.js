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

function findHospitals() {
    let radius = document.getElementById("radius").value;
    const customRadius = document.getElementById("custom-radius").value;
    if (customRadius) {
        radius = customRadius;
    }

    const typeElement = document.getElementById("type");
    if (!typeElement) {
        alert("Не найден элемент для типа учреждения.");
        return;
    }
    const type = typeElement.value;
    const keyword = type;

    const minRatingElement = document.getElementById("min-rating");
    const minRating = minRatingElement.value;

    if (!userMarker) {
        alert("Не удалось определить ваше местоположение.");
        return;
    }

    const lat = userMarker.getPosition().lat();
    const lng = userMarker.getPosition().lng();

    fetch(`/find-hospitals/?lat=${lat}&lng=${lng}&radius=${radius}&type=${type}&keyword=${keyword}&min_rating=${minRating}`)
        .then(response => response.json())
        .then(data => {
            if (data.hospitals) {
                displayHospitals(data.hospitals);
            } else {
                alert("Медицинские учреждения не найдены.");
            }
        })
        .catch(error => console.error("Ошибка при получении данных:", error));
}

function displayHospitals(hospitals) {
    const container = document.getElementById("hospitals");
    container.innerHTML = "";

    const placesService = new google.maps.places.PlacesService(map);

    hospitals.forEach(hospital => {
        const card = document.createElement("div");
        card.className = "hospital-card";
        card.innerHTML = `
            <h3>${hospital.name}</h3>
            <p>Адрес: ${hospital.address}</p>
            <p>Координаты: ${hospital.lat}, ${hospital.lng}</p>
            <div id="rating-${hospital.place_id}"></div> <button onclick="openInGoogleMaps(${hospital.lat}, ${hospital.lng}, '${hospital.name}')">Открыть в Google Maps</button>
        `;
        container.appendChild(card);

        const hospitalMarker = new google.maps.Marker({
            position: { lat: hospital.lat, lng: hospital.lng },
            map: map,
            title: hospital.name
        });

        // Получаем детали места, включая рейтинг
        placesService.getDetails({
            placeId: hospital.place_id, // Предполагается, что Place ID есть в данных о больнице
            fields: ['rating']
        }, (place, status) => {
            if (status === google.maps.places.PlacesServiceStatus.OK && place.rating) {
                const ratingContainer = document.getElementById(`rating-${hospital.place_id}`);
                ratingContainer.textContent = `Рейтинг: ${place.rating} ⭐`; // Простое отображение рейтинга
            }
        });

        // Выделение при наведении
        hospitalMarker.addListener('mouseover', () => {
            hospitalMarker.setIcon('URL_АНИМИРОВАННОЙ_ИЛИ_ВЫДЕЛЕННОЙ_ИКОНКИ');
        });
        hospitalMarker.addListener('mouseout', () => {
            hospitalMarker.setIcon(null); // Возвращаем к стандартной иконке
        });

        // Открытие InfoWindow или Google Maps при клике
        hospitalMarker.addListener('click', () => {
            // Пример открытия InfoWindow
            const infoWindow = new google.maps.InfoWindow({
                content: `<div><h3>${hospital.name}</h3><p>Рейтинг: ${place && place.rating ? place.rating + ' ⭐' : 'Нет рейтинга'}</p><button onclick="openInGoogleMaps(${hospital.lat}, ${hospital.lng}, '${hospital.name}')">Открыть в Google Maps</button></div>`
            });
            infoWindow.open(map, hospitalMarker);
        });
    });
}

function openInGoogleMaps(lat, lng, name) {
    const url = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(name)}&ll=${lat},${lng}`;
    window.open(url, '_blank');
}