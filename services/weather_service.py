import requests
from config import WEATHER_API_KEY, CITY


WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'
PARAMS = {
        'q': CITY,
        'appid': WEATHER_API_KEY,
        'units': 'metric',
        'lang': 'ru'
    }


class WeatherService:
    
    def get_weather(self):
        try:
            response = requests.get(WEATHER_URL, timeout=5, params=PARAMS)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException:
            return None
