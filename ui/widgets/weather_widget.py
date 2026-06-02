from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from ui.widgets.card import Card
from services.weather_service import WeatherService


class WeatherWidget(Card):
    def __init__(self, weather_service: WeatherService):
        self.weather_service = weather_service

        weather_body = QWidget()
        weather_layout = QHBoxLayout(weather_body)
        weather_layout.setContentsMargins(0, 0, 0, 0)
        weather_layout.setSpacing(14)

        self.weather_icon = QLabel("☀️")
        self.weather_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.weather_icon.setFont(QFont("Segoe UI", 28))

        self.weather_text = QLabel("+18°C\nЯсно")
        self.weather_text.setWordWrap(True)
        self.weather_text.setObjectName("cardText")

        weather_layout.addWidget(self.weather_icon)
        weather_layout.addWidget(self.weather_text)

        super().__init__("Погода", body_widget=weather_body)

        self.load_weather()

    def load_weather(self):

        weather = self.weather_service.get_weather()

        if not isinstance(weather, dict):
            self.weather_text.setText(
                "Не удалось получить погоду"
            )
            return

        try:

            temp = round(weather["main"]["temp"])
            status = weather["weather"][0]["description"]

            self.weather_text.setText(
                f"{temp}°C\n{status.capitalize()}"
            )

            weather_type = weather["weather"][0]["main"]

            self.update_weather_icon(weather_type)

        except (KeyError, TypeError):
            self.weather_text.setText(
                "Ошибка данных погоды"
            )

    def update_weather_icon(self, weather_type):

        icons = {
            "Clear": "☀️",
            "Clouds": "☁️",
            "Rain": "🌧️",
            "Snow": "❄️",
            "Thunderstorm": "⛈️"
        }

        self.weather_icon.setText(
            icons.get(weather_type, "🌤️")
        )
