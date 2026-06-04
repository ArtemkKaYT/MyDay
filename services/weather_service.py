import requests
import config

WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'


class WeatherService:  # Сервис для получения погоды с OpenWeatherMap

    def get_weather(self):  # Запрашивает текущую погоду для города из конфига
        params = {
            'q': config.get_city(),
            'appid': config.get_weather_api_key(),
            'units': 'metric',
            'lang': 'ru'
        }

        if not params['appid']:  # Проверка наличия API ключа
            return None

        try:
            response = requests.get(WEATHER_URL, timeout=5, params=params)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException:  # Обработка ошибок сети/API
            return None
