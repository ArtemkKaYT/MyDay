"""
Модуль виджета для отображения информации о погоде (Weather Widget).

Этот модуль содержит функциональность для получения, отображения и управления
информацией о погоде с помощью OpenWeatherMap API.

Включает:
- WeatherWidget: Виджет для отображения текущей погоды
- WeatherSettingsDialog: Диалоговое окно для настройки API ключа и города
- Функции для чтения и записи настроек в файл .env

Пример:
    Использование WeatherWidget::

        from ui.widgets.weather_widget import WeatherWidget
        from services.weather_service import WeatherService

        weather_service = WeatherService()
        widget = WeatherWidget(weather_service)
        widget.show()
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


def read_env_settings():
    """
    Читать настройки из файла .env.

    Получает значения API ключа и города из файла конфигурации .env.

    Возвращает:
        dict: Словарь с ключами 'WEATHER_API_KEY' и 'CITY'. Если файла
              нет или ключ отсутствует, возвращает значение по умолчанию.
    """
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


def write_env_settings(api_key, city):
    """
    Записать настройки в файл .env.

    Сохраняет API ключ и название города в файл конфигурации .env.
    Если файл не существует, создаёт новый.

    Аргументы:
        api_key (str): OpenWeatherMap API ключ.
        city (str): Название города для запросов о погоде.
    """
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


class WeatherSettingsDialog(QDialog):
    """
    Диалоговое окно для настройки параметров погоды.

    Позволяет пользователю устанавливать API ключ OpenWeatherMap
    и выбирать город для получения информации о погоде.

    Атрибуты:
        api_input (QLineEdit): Поле для ввода API ключа
        city_input (QLineEdit): Поле для ввода названия города
        button_box (QDialogButtonBox): Кнопки сохранения и отмены
    """

    def __init__(self, parent=None):
        """
        Инициализация WeatherSettingsDialog.

        Создаёт диалоговое окно с полями для API ключа и города.

        Аргументы:
            parent (QWidget, optional): Родительский виджет.
        """
        super().__init__(parent)
        self.setWindowTitle("Настройки погоды")
        self.setModal(True)
        self.setFixedWidth(320)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        form_layout = QFormLayout()
        form_layout.setSpacing(8)

        # Поле ввода для API ключа
        self.api_input = QLineEdit()
        self.api_input.setPlaceholderText("Вставьте API ключ OpenWeather")

        # Поле ввода для названия города
        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Например: Saint Petersburg")

        form_layout.addRow("API Ключ:", self.api_input)
        form_layout.addRow("Город:", self.city_input)
        layout.addLayout(form_layout)

        # Кнопки сохранения и отмены
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save |
            QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.accepted.connect(self.save_and_close)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        # Загружаем текущие настройки
        self.load_current_settings()

    def load_current_settings(self):
        """
        Загрузить текущие настройки в поля формы.

        Получает текущие значения API ключа и города из файла .env
        и устанавливает их в соответствующие поля ввода.
        """
        data = read_env_settings()
        self.api_input.setText(data["WEATHER_API_KEY"])
        self.city_input.setText(data["CITY"])

    def save_and_close(self):
        """
        Сохранить настройки и закрыть диалоговое окно.

        Получает значения из полей, валидирует их, сохраняет в файл .env
        и закрывает диалоговое окно.
        """
        api = self.api_input.text().strip()
        city = self.city_input.text().strip()
        if not city:
            city = "Saint Petersburg"

        write_env_settings(api, city)
        self.accept()


class WeatherWidget(Card):
    """
    Виджет для отображения информации о текущей погоде.

    Получает и отображает текущую температуру, описание погоды,
    и иконку, соответствующую типу погоды. Содержит кнопку для
    открытия диалога настроек.

    Атрибуты:
        weather_service (WeatherService): Сервис для получения данных о погоде
        weather_icon (QLabel): Иконка текущей погоды (эмодзи)
        weather_text (QLabel): Отображаемая температура
        status_label (QLabel): Описание погоды
        settings_button (QPushButton): Кнопка открытия диалога настроек

    Сигналы:
        settings_changed: Испускается при изменении настроек погоды
    """

    settings_changed = pyqtSignal()

    def __init__(self, weather_service: WeatherService):
        """
        Инициализация WeatherWidget.

        Создаёт виджет с отображением погоды и кнопкой настроек.

        Аргументы:
            weather_service (WeatherService): Экземпляр сервиса погоды.
        """
        self.weather_service = weather_service

        # Создаём контейнер для погоды
        weather_body = QWidget()
        weather_layout = QHBoxLayout(weather_body)
        weather_layout.setContentsMargins(0, 0, 0, 0)
        weather_layout.setSpacing(14)

        # Иконка погоды
        self.weather_icon = QLabel("☀️")
        self.weather_icon.setFixedWidth(50)
        self.weather_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.weather_icon.setObjectName("weatherIcon")

        # Контейнер для текста температуры и описания
        text_container = QWidget()
        text_layout = QVBoxLayout(text_container)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(2)

        # Температура
        self.weather_text = QLabel("+18°C")
        self.weather_text.setObjectName("weatherTemp")

        # Описание погоды
        self.status_label = QLabel("Ясно")
        self.status_label.setWordWrap(True)
        self.status_label.setObjectName("weatherStatus")

        text_layout.addWidget(self.weather_text)
        text_layout.addWidget(self.status_label)

        # Кнопка настроек
        self.settings_button = QPushButton("⚙️")
        self.settings_button.setObjectName("weatherSettingsBtn")
        self.settings_button.setFixedSize(26, 26)
        self.settings_button.clicked.connect(self.open_settings)

        # Размещаем элементы
        weather_layout.addWidget(self.weather_icon)
        weather_layout.addWidget(text_container)
        weather_layout.addStretch()
        weather_layout.addWidget(self.settings_button)

        # Инициализируем родительский класс Card
        super().__init__("Погода", body_widget=weather_body)
        
        # Загружаем текущую погоду
        self.load_weather()

    def open_settings(self):
        """
        Открыть диалоговое окно настроек.

        Открывает диалог для настройки API ключа и города,
        затем перезагружает погоду если настройки были сохранены.
        """
        dialog = WeatherSettingsDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_weather()
            self.settings_changed.emit()

    def load_weather(self):
        """
        Загрузить и отобразить текущую погоду.

        Получает данные о погоде из сервиса, обновляет температуру,
        описание и иконку. При ошибке соединения показывает
        соответствующее сообщение.
        """
        weather = self.weather_service.get_weather()

        if not isinstance(weather, dict):
            self.weather_text.setText("--")
            self.status_label.setText("Ошибка соединения")
            return

        try:
            # Получаем температуру и округляем
            temp = round(weather["main"]["temp"])
            status = weather["weather"][0]["description"]

            # Добавляем знак + для положительных температур
            sign = "+" if temp > 0 else ""

            self.weather_text.setText(f"{sign}{temp}°C")
            self.status_label.setText(status.capitalize())

            # Обновляем иконку в зависимости от типа погоды
            weather_type = weather["weather"][0]["main"]
            self.update_weather_icon(weather_type)

        except (KeyError, TypeError):
            self.weather_text.setText("--")
            self.status_label.setText("Ошибка данных")

    def update_weather_icon(self, weather_type):
        """
        Обновить иконку погоды в зависимости от типа.

        Аргументы:
            weather_type (str): Тип погоды (Clear, Clouds, Rain, Snow, Thunderstorm и т.д.)
        """
        icons = {
            "Clear": "☀️", "Clouds": "☁️", "Rain": "🌧️",
            "Snow": "❄️", "Thunderstorm": "⛈️"
        }
        self.weather_icon.setText(icons.get(weather_type, "🌤️"))
