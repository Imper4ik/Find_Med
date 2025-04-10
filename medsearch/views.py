# Импорт необходимых библиотек
from django.shortcuts import render
from Find_Med.settings import GOOGLE_API_KEY
from django.http import JsonResponse
from django.conf import settings
import requests
import logging

# Настроим логирование
logger = logging.getLogger(__name__)

# Индексная страница
def index(request):
    context = {
        'google_api_key': GOOGLE_API_KEY
    }
    return render(request, 'medsearch/index.html', context)

# Функция для поиска больниц с учетом рейтинга
def find_hospitals(request):
    try:
        # Получаем параметры lat, lng, radius, type, keyword и min_rating из GET-запроса
        lat = float(request.GET.get('lat'))
        lng = float(request.GET.get('lng'))
        radius = int(request.GET.get('radius', 5000))  # Радиус по умолчанию 5000 метров
        keyword = request.GET.get('keyword', '')  # Ключевое слово
        type_filter = request.GET.get('type', 'hospital')  # Тип учреждения по умолчанию - hospital
        min_rating = float(request.GET.get('min_rating', 0))  # Минимальный рейтинг по умолчанию 0

        # Ваш ключ API Google
        api_key = settings.GOOGLE_API_KEY

        # URL для запроса Google Places API с учетом типа, ключевого слова и минимального рейтинга
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&type={type_filter}&keyword={keyword}&min_rating={min_rating}&key={api_key}"

        # Получение данных с API
        response = requests.get(url)

        # Проверяем, успешен ли запрос
        if response.status_code != 200:
            return JsonResponse({"error": "Не удалось получить данные от Google API"}, status=500)

        data = response.json()
        hospitals = []
        for result in data.get('results', []):
            rating = result.get('rating')
            if rating is not None and rating >= min_rating:  # Фильтрация здесь
                hospital = {
                    'name': result.get('name'),
                    'address': result.get('vicinity'),
                    'lat': result['geometry']['location']['lat'],
                    'lng': result['geometry']['location']['lng'],
                    'rating': rating,
                    'place_id': result.get('place_id')
                }
                hospitals.append(hospital)
        return JsonResponse({'hospitals': hospitals})
    except Exception as e:
        logger.error(f"Error finding hospitals: {e}")
        return JsonResponse({"error": "Произошла ошибка на сервере"}, status=500)

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