"""
Модуль главного окна приложения MyDay.

Этот модуль содержит главное окно приложения, которое объединяет все виджеты:

- Виджет с часами и датой
- Виджет с ежедневной сводкой
- Виджет с информацией о погоде
- Виджет с расписанием событий
- Виджет с заметками

Главное окно также управляет темой оформления на основе текущей погоды
и запускает анимации для плавного появления элементов интерфейса.

Пример:
    Создание и отображение главного окна::

        from ui.main_window import MainWindow
        from PyQt6.QtWidgets import QApplication
        import sys

        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
"""

from PyQt6.QtCore import QTimer, QPropertyAnimation, QThread, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea

from ui.widgets.header_widget import HeaderWidget
from ui.widgets.brief_widget import BriefWidget
from ui.widgets.weather_widget import WeatherWidget
from ui.widgets.schedule_widget import ScheduleWidget
from ui.widgets.notes_widget import NotesWidget

from services.weather_service import WeatherService
from services.schedule_service import ScheduleService
from services.notes_service import NotesService
from services.brief_service import BriefService

from ui.styles.theme_meneger import get_weather_theme


class WeatherFetchWorker(QThread):
    """
    Рабочий поток для асинхронного получения данных о погоде.

    Этот класс запускает запрос к API погоды в отдельном потоке,
    чтобы не заблокировать главный UI поток приложения.

    Сигналы:
        finished (dict): Испускается когда данные о погоде успешно получены
    """

    finished = pyqtSignal(dict)

    def __init__(self, weather_service):
        """
        Инициализация WeatherFetchWorker.

        Аргументы:
            weather_service (WeatherService): Экземпляр сервиса погоды.
        """
        super().__init__()
        self.weather_service = weather_service

    def run(self):
        """
        Получить данные о погоде и испустить сигнал.

        Этот метод вызывается при запуске потока.
        Получает данные и испускает сигнал finished если данные успешно получены.
        """
        data = self.weather_service.get_weather()
        if data:
            self.finished.emit(data)


class MainWindow(QWidget):
    """
    Главное окно приложения MyDay.

    Этот класс создаёт главное окно приложения, инициализирует все сервисы,
    создаёт и размещает все виджеты интерфейса, управляет темой оформления
    в зависимости от погоды и запускает анимации для плавного появления элементов.

    Атрибуты:
        weather_service (WeatherService): Сервис для получения данных о погоде
        schedule_service (ScheduleService): Сервис для управления расписанием
        notes_service (NotesService): Сервис для управления заметками
        brief_service (BriefService): Сервис для генерации ежедневной сводки
        header_widget (HeaderWidget): Виджет с часами и датой
        brief_widget (BriefWidget): Виджет со сводкой дня
        weather_widget (WeatherWidget): Виджет с информацией о погоде
        schedule_widget (ScheduleWidget): Виджет с расписанием
        notes_widget (NotesWidget): Виджет с заметками
    """

    def __init__(self):
        """
        Инициализация главного окна.

        Инициализирует все сервисы, создаёт виджеты, размещает их
        в скроллируемой области, и запускает загрузку темы и анимаций.
        """
        super().__init__()

        # Инициализируем все сервисы
        self.weather_service = WeatherService()
        self.schedule_service = ScheduleService()
        self.notes_service = NotesService()

        self.brief_service = BriefService(
            self.weather_service,
            self.schedule_service
        )

        # Настройка окна
        self.setWindowTitle("MyDay")
        self.resize(720, 860)

        self.animations = []

        # Устанавливаем тему по умолчанию
        self.setStyleSheet(get_weather_theme("Clouds"))

        # Создаём главный макет
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        # Создаём скроллируемую область
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        scroll_content = QWidget()

        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(24, 24, 24, 24)
        scroll_layout.setSpacing(16)

        # Создаём и добавляем виджет с часами и датой
        self.header_widget = HeaderWidget()
        scroll_layout.addWidget(self.header_widget)

        # Создаём и добавляем виджет со сводкой
        self.brief_widget = BriefWidget(self.brief_service)
        scroll_layout.addWidget(self.brief_widget)

        # Создаём и добавляем виджет с погодой
        self.weather_widget = WeatherWidget(self.weather_service)
        scroll_layout.addWidget(self.weather_widget)

        # Подключаем сигнал изменения настроек к обновлению темы
        self.weather_widget.settings_changed.connect(self.load_weather_theme_async)

        scroll_layout.addWidget(self.weather_widget)

        # Создаём и добавляем виджет с расписанием
        self.schedule_widget = ScheduleWidget(self.schedule_service)
        scroll_layout.addWidget(self.schedule_widget)

        # Создаём и добавляем виджет с заметками
        self.notes_widget = NotesWidget(self.notes_service)
        scroll_layout.addWidget(self.notes_widget)

        scroll_layout.addStretch()

        scroll_area.setWidget(scroll_content)
        root.addWidget(scroll_area)

        # Загружаем тему на основе текущей погоды
        self.load_weather_theme_async()

        # Запускаем анимации появления элементов
        self.start_animations()

    def load_weather_theme_async(self):
        """
        Загрузить тему оформления на основе текущей погоды асинхронно.

        Запускает рабочий поток для получения данных о погоде,
        затем применяет соответствующую тему к главному окну.
        """
        self.weather_worker = WeatherFetchWorker(self.weather_service)

        self.weather_worker.finished.connect(self.on_weather_loaded)

        self.weather_worker.start()

    def on_weather_loaded(self, weather_data):
        """
        Обновить тему оформления после получения данных о погоде.

        Аргументы:
            weather_data (dict): Словарь данных о погоде из API.
        """
        try:
            weather_main = weather_data["weather"][0]["main"]

            new_style = get_weather_theme(weather_main)

            self.setStyleSheet(new_style)

        except (KeyError, IndexError):
            pass

    def start_animations(self):
        """
        Запустить анимации появления элементов интерфейса.

        Запускает последовательные анимации прозрачности для разных
        виджетов, создавая плавный эффект появления при загрузке.
        """
        # Запускаем анимацию печати текста сводки
        QTimer.singleShot(300, self.brief_widget.start_animation)

        # Список карточек для анимирования
        cards = [self.weather_widget, self.schedule_widget, self.notes_widget]

        for index, card in enumerate(cards):
            def show_card(c=card):
                animation = QPropertyAnimation(c.graphicsEffect(), b"opacity")
                animation.setDuration(700)
                animation.setStartValue(0)
                animation.setEndValue(1)
                animation.start()
                self.animations.append(animation)

            QTimer.singleShot(1200 + index * 350, show_card)
