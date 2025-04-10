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
        api_key = settings.GOOGLE_API_KEY # Используем GOOGLE_API_KEY из settings

        # URL для запроса Google Places API (Nearby Search)
        # Запрашиваем базовые поля + 'website' и 'formatted_phone_number', если они нужны
        # Примечание: Nearby Search не всегда возвращает 'website'. Для гарантированного получения
        # может потребоваться дополнительный запрос Place Details, но это усложнит код.
        # Попробуем получить его из Nearby Search.
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&type={type_filter}&keyword={keyword}&key={api_key}"
        # Если нужно гарантированно получать больше полей, можно добавить '&fields=...'
        # но для Nearby Search это не стандартный параметр.

        # Получение данных с API
        response = requests.get(url)

        # Проверяем, успешен ли запрос
        if response.status_code != 200:
            logger.error(f"Google API request failed with status {response.status_code}: {response.text}")
            return JsonResponse({"error": "Не удалось получить данные от Google API"}, status=500)

        data = response.json()
        hospitals = []

        # Добавим проверку статуса ответа API
        api_status = data.get('status')
        if api_status != 'OK' and api_status != 'ZERO_RESULTS':
             logger.error(f"Google API returned status {api_status}: {data.get('error_message', '')}")
             # Можно вернуть более информативную ошибку пользователю или просто пустой список
             # return JsonResponse({"error": f"Ошибка Google API: {api_status}"}, status=500)


        for result in data.get('results', []):
            rating = result.get('rating')
            # Применяем фильтр по рейтингу уже после получения результатов
            if rating is not None and rating < min_rating:
                 continue # Пропускаем учреждение, если рейтинг ниже минимального

            # Формируем словарь с данными об учреждении
            hospital = {
                'name': result.get('name'),
                'address': result.get('vicinity'), # 'vicinity' обычно содержит адрес
                'lat': result['geometry']['location']['lat'],
                'lng': result['geometry']['location']['lng'],
                'rating': rating,
                'place_id': result.get('place_id'),
                # --- Добавляем веб-сайт ---
                'website': result.get('website', None), # Получаем веб-сайт, если он есть
                'url': result.get('url', None)
                # --------------------------
            }
            hospitals.append(hospital)

        return JsonResponse({'hospitals': hospitals})

    except Exception as e:
        logger.exception("Error in find_hospitals view") # Логируем полное исключение
        return JsonResponse({"error": "Произошла внутренняя ошибка сервера"}, status=500)

# Эндпоинт для расчета расстояния до больницы (сейчас не используется фронтендом)
def calculate_distance(request):
    # ... (остальной код этой функции без изменений) ...
    lat1 = float(request.GET.get('lat1'))
    lon1 = float(request.GET.get('lon1'))
    lat2 = float(request.GET.get('lat2'))
    lon2 = float(request.GET.get('lon2'))

    import math
    R = 6371
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    distance_in_meters = distance * 1000

    return JsonResponse({'distance': distance_in_meters})