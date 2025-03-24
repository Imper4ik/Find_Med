from django.shortcuts import render
from django.http import JsonResponse
import requests

from University_Project.settings import GOOGLE_API_KEY


# Индексная страница
def index(request):
    context = {
        'google_api_key': GOOGLE_API_KEY
    }
    return render(request, 'medsearch/index.html', context)


# Эндпоинт для поиска больниц
def find_hospitals(request):
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')
    radius = request.GET.get('radius', 5000)  # Радиус по умолчанию 5000 метров

    # Пример запроса в Google Places API для поиска больниц
    api_key = GOOGLE_API_KEY
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius={radius}&type=hospital&key={api_key}"

    response = requests.get(url)
    data = response.json()

    hospitals = [
        {
            'name': hospital['name'],
            'address': hospital.get('vicinity', 'Не указано'),
            'latitude': hospital['geometry']['location']['lat'],
            'longitude': hospital['geometry']['location']['lng']
        }
        for hospital in data['results']
    ]

    return JsonResponse({'hospitals': hospitals})


# Эндпоинт для расчета расстояния до больницы
def calculate_distance(request):
    lat1 = float(request.GET.get('lat1'))
    lon1 = float(request.GET.get('lon1'))
    lat2 = float(request.GET.get('lat2'))
    lon2 = float(request.GET.get('lon2'))

    # Пример расчета по формуле Haversine
    import math
    R = 6371  # Радиус Земли в км
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c  # Расстояние в км
    distance_in_meters = distance * 1000  # Переводим в метры

    return JsonResponse({'distance': distance_in_meters})
