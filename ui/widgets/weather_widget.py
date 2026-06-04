"""
@file theme_meneger.py
@brief Module of MyDay project.
"""
from pathlib import Path
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QVBoxLayout, QWidget, QHBoxLayout, QLabel,
    QPushButton, QDialog, QFormLayout, QLineEdit, QDialogButtonBox
)
from ui.widgets.card import Card
from services.weather_service import WeatherService


ENV_PATH = Path(".env")


def read_env_settings():  # Читает API ключ и город из .env
    settings = {"WEATHER_API_KEY": "", "CITY": "Saint Petersburg"}
    if ENV_PATH.exists():
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    if k in settings:
                        settings[k] = v
    return settings

def write_env_settings(api_key, city):  # Сохраняет настройки в .env файл
    lines = []
    keys_updated = {"WEATHER_API_KEY": False, "CITY": False}
    
    if ENV_PATH.exists():
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.strip().startswith("#"):
                    k, _ = line.split("=", 1)
                    k = k.strip()

                    if k == "WEATHER_API_KEY":
                        lines.append(f"WEATHER_API_KEY='{api_key}'\n")
                        keys_updated["WEATHER_API_KEY"] = True
                        continue
                    elif k == "CITY":
                        lines.append(f"CITY='{city}'\n")
                        keys_updated["CITY"] = True
                        continue

                lines.append(line)

    if lines and not lines[-1].endswith("\n"):
        lines[-1] += "\n"

    if not keys_updated["WEATHER_API_KEY"]:
        lines.append(f"WEATHER_API_KEY='{api_key}'\n")
    if not keys_updated["CITY"]:
        lines.append(f"CITY='{city}'\n")

    with open(ENV_PATH, "w", encoding="utf-8") as f:
        f.writelines(lines)


class WeatherSettingsDialog(QDialog):  # Диалоговое окно настроек погоды
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки погоды")
        self.setModal(True)
        self.setFixedWidth(320)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        form_layout = QFormLayout()
        form_layout.setSpacing(8)

        self.api_input = QLineEdit()
        self.api_input.setPlaceholderText("Вставьте API ключ OpenWeather")

        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Например: Saint Petersburg")

        form_layout.addRow("API Ключ:", self.api_input)
        form_layout.addRow("Город:", self.city_input)
        layout.addLayout(form_layout)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save |
            QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.accepted.connect(self.save_and_close)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self.load_current_settings()

    def load_current_settings(self):  # Загружает текущие настройки в поля
        data = read_env_settings()
        self.api_input.setText(data["WEATHER_API_KEY"])
        self.city_input.setText(data["CITY"])

    def save_and_close(self):  # Сохраняет настройки и закрывает диалог
        api = self.api_input.text().strip()
        city = self.city_input.text().strip()
        if not city:
            city = "Saint Petersburg"

        write_env_settings(api, city)
        self.accept()


class WeatherWidget(Card):  # Виджет отображения погоды
    settings_changed = pyqtSignal()

    def __init__(self, weather_service: WeatherService):
        self.weather_service = weather_service

        weather_body = QWidget()
        weather_layout = QHBoxLayout(weather_body)
        weather_layout.setContentsMargins(0, 0, 0, 0)
        weather_layout.setSpacing(14)

        self.weather_icon = QLabel("☀️")
        self.weather_icon.setFixedWidth(50)
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

        self.settings_button = QPushButton("⚙️")
        self.settings_button.setObjectName("weatherSettingsBtn")
        self.settings_button.setFixedSize(26, 26)
        self.settings_button.clicked.connect(self.open_settings)

        weather_layout.addWidget(self.weather_icon)
        weather_layout.addWidget(text_container)
        weather_layout.addStretch()
        weather_layout.addWidget(self.settings_button)

        super().__init__("Погода", body_widget=weather_body)
        self.load_weather()

    def open_settings(self):  # Открывает диалог настроек
        dialog = WeatherSettingsDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_weather()
            self.settings_changed.emit()

    def load_weather(self):  # Загружает и отображает текущую погоду
        weather = self.weather_service.get_weather()

        if not isinstance(weather, dict):
            self.weather_text.setText("--")
            self.status_label.setText("Ошибка соединения")
            return

        try:
            temp = round(weather["main"]["temp"])
            status = weather["weather"][0]["description"]

            sign = "+" if temp > 0 else ""

            self.weather_text.setText(f"{sign}{temp}°C")
            self.status_label.setText(status.capitalize())

            weather_type = weather["weather"][0]["main"]
            self.update_weather_icon(weather_type)

        except (KeyError, TypeError):
            self.weather_text.setText("--")
            self.status_label.setText("Ошибка данных")

    def update_weather_icon(self, weather_type):  # Обновляет иконку по типу погоды
        icons = {
            "Clear": "☀️", "Clouds": "☁️", "Rain": "🌧️",
            "Snow": "❄️", "Thunderstorm": "⛈️"
        }
        self.weather_icon.setText(icons.get(weather_type, "🌤️"))
