"""
Модуль сервиса погоды (Weather Service) для приложения MyDay.

Этот модуль обеспечивает интеграцию с API OpenWeatherMap для получения
данных о погоде в реальном времени для настроенного города.

Класс WeatherService обрабатывает все операции, связанные с погодой, включая:

- Получение текущих условий погоды
- Обработка ошибок при сбоях API
- Управление таймаутом запросов и кешированием

Пример:
    Использование WeatherService::

        from services.weather_service import WeatherService

        weather_service = WeatherService()
        weather_data = weather_service.get_weather()
        if weather_data:
            print(weather_data['weather'][0]['main'])

Атрибуты:
    WEATHER_URL (str): Endpoint API OpenWeatherMap для текущей погоды
"""

import requests
import config

# API endpoint OpenWeatherMap для получения данных о текущей погоде
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'


class WeatherService:
    """
    Сервис для получения информации о погоде из API OpenWeatherMap.

    Этот класс предоставляет методы для получения текущих условий погоды
    для настроенного города, используя OpenWeatherMap API.
    Включает обработку ошибок для проблем сети и отсутствия учётных данных.

    Атрибуты:
        weather_url (str): URL endpoint API (константа класса)

    Пример:
        Получение данных о погоде::

            service = WeatherService()
            weather = service.get_weather()
            if weather:
                temperature = weather['main']['temp']
                description = weather['weather'][0]['description']
    """

    def get_weather(self):
        """
        Получить текущие данные о погоде для настроенного города.

        Делает HTTP запрос к API OpenWeatherMap, используя учётные данные
        из конфигурации. Возвращает данные о погоде, включая температуру,
        условия, влажность и информацию о ветре.

        Запрос включает:
        - Город из конфигурации (по умолчанию: Saint Petersburg)
        - API ключ из переменных окружения
        - Температура в Цельсиях
        - Ответ на русском языке

        Возвращает:
            dict: Словарь данных о погоде с ключами 'weather', 'main',
                  'wind', 'clouds' и т.д. Возвращает None если API ключ
                  не установлен или произошла ошибка сети/API.

        Исключения:
            None: Исключения перехватываются и вместо них возвращается None.

        Примечание:
            - Таймаут запроса установлен на 5 секунд
            - Возвращает None если WEATHER_API_KEY не настроена
            - Ошибки сети обрабатываются молча (возвращается None)

        Пример:
            Получение данных о погоде::

                weather = service.get_weather()
                if weather:
                    condition = weather['weather'][0]['main']
                    temp = weather['main']['temp']
        """
        params = {
            'q': config.get_city(),
            'appid': config.get_weather_api_key(),
            'units': 'metric',
            'lang': 'ru'
        }

        # Проверяем, установлен ли API ключ
        if not params['appid']:
            return None

        try:
            response = requests.get(WEATHER_URL, timeout=5, params=params)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException:
            # Ошибка сети или API - возвращаем None вместо выброса исключения
            return None
