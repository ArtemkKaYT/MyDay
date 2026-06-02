from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QLabel
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
        self.weather_icon.setObjectName("weatherIcon")

        text_container = QWidget()
        text_layout = QVBoxLayout(text_container)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(2)

        self.weather_text = QLabel("+18°C")
        self.weather_text.setObjectName("weatherTemp")

        self.status_label = QLabel("Ясно")
        self.status_label.setWordWrap(True)
        self.status_label.setObjectName("weatherStatus")

        text_layout.addWidget(self.weather_text)
        text_layout.addWidget(self.status_label)

        weather_layout.addWidget(self.weather_icon)
        weather_layout.addWidget(text_container)
        weather_layout.addStretch()

        super().__init__("Погода", body_widget=weather_body)

        self.load_weather()

    def load_weather(self):
        weather = self.weather_service.get_weather()

        if not isinstance(weather, dict):
            self.weather_text.setText("--")
            self.status_label.setText("Ошибка соединения")
            return

        try:
            temp = round(weather["main"]["temp"])
            status = weather["weather"][0]["description"]

            # ИСПРАВЛЕНИЕ: убираем \n и раскладываем текст по полочкам
            sign = "+" if temp > 0 else ""
            
            self.weather_text.setText(f"{sign}{temp}°C")    # Только температура
            self.status_label.setText(status.capitalize()) # Меняет "Ясно" на актуальный статус (например, "Пасмурно")

            weather_type = weather["weather"][0]["main"]
            self.update_weather_icon(weather_type)

        except (KeyError, TypeError):
            self.weather_text.setText("--")
            self.status_label.setText("Ошибка данных")

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
